#!/usr/bin/env bash
# Replace localhost / 127.0.0.1 with a target host across the frontend tree.
# Usage:  ./scripts/swap-host.sh <new-host>          # in-place edit
#         ./scripts/swap-host.sh <new-host> --dry    # print what would change
#
# Edits .ts/.tsx/.js/.jsx/.json/.env* under frontend/akiora-v4, excluding
# node_modules, dist, build, .next, .git. Ports are preserved — only the host
# part changes. Examples:
#   http://localhost:8000   -> http://185.88.101.251:8000
#   http://127.0.0.1:5173   -> http://185.88.101.251:5173
#
# Re-runnable: doing it twice does nothing extra.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <new-host> [--dry]" >&2
  exit 2
fi

NEW_HOST="$1"
DRY="${2:-}"

# Repo root = parent of this script's directory (frontend/akiora-v4).
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Files to consider — .env* matched separately because globs+find are awkward.
mapfile -d '' FILES < <(
  find "$ROOT" \
    -type d \( -name node_modules -o -name dist -o -name build -o -name .next -o -name .git -o -name .turbo -o -name coverage \) -prune \
    -o -type f \( \
        -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' \
     -o -name '*.json' -o -name '*.html' -o -name '*.md' \
     -o -name '.env' -o -name '.env.*' \
    \) -print0
)

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "no candidate files under $ROOT" >&2
  exit 0
fi

# Match localhost or 127.0.0.1 only when preceded by // (i.e. inside a URL).
# Anchoring on // avoids hitting comments like "talks to localhost" in prose,
# while still catching http://, https://, ws://, wss://, postgres://, etc.
PATTERN='(\b(?:[a-zA-Z][a-zA-Z0-9+.-]*):\/\/)(?:localhost|127\.0\.0\.1)\b'
REPL="\${1}${NEW_HOST}"

CHANGED=0
for f in "${FILES[@]}"; do
  # Skip binary / unreadable.
  [[ -r "$f" ]] || continue
  if ! grep -qE 'localhost|127\.0\.0\.1' "$f" 2>/dev/null; then
    continue
  fi
  # Use perl for PCRE + in-place edit that's identical on Linux & macOS.
  if [[ "$DRY" == "--dry" ]]; then
    if perl -ne "BEGIN{\$h='${NEW_HOST}'} print \"$f:\$.: \$_\" if s|${PATTERN}|\${1}\$h|g" "$f"; then :; fi
  else
    BEFORE_HASH=$(perl -ne 'print' "$f" | md5sum | awk '{print $1}')
    perl -i -pe "BEGIN{\$h='${NEW_HOST}'} s|${PATTERN}|\${1}\$h|g" "$f"
    AFTER_HASH=$(perl -ne 'print' "$f" | md5sum | awk '{print $1}')
    if [[ "$BEFORE_HASH" != "$AFTER_HASH" ]]; then
      echo "patched: ${f#$ROOT/}"
      CHANGED=$((CHANGED+1))
    fi
  fi
done

if [[ "$DRY" == "--dry" ]]; then
  echo "(dry run — nothing written)"
else
  echo "done. files patched: $CHANGED"
  echo "next: restart the Vite dev server so it re-reads .env"
fi
