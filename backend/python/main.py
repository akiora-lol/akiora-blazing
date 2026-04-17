import os
import re
import sys
import subprocess
from pathlib import Path


def find_proto_files(root_dir: Path):
    """Рекурсивно находит все .proto файлы"""
    l = list(root_dir.rglob("*.proto"))
    l = [p for p in l if "googleapis" not in p.as_uri().split("/")]
    l = [
        p
        for p in l
        if "google" not in p.as_uri().split("/") or ("api" in p.as_uri().split("/"))
    ]
    print(l)

    return l


def main():

    proto_root = Path("../proto").resolve()

    output_dirs = [
        Path("game").resolve(),
    ]
    googleapis_path = proto_root / "googleapis"

    print(f"Proto source directory : {proto_root}")
    print(f"Output directory      : {output_dirs}\n")
    for output_dir in output_dirs:
        output_dir.mkdir(parents=True, exist_ok=True)

    proto_files = find_proto_files(proto_root)

    if not proto_files:
        print(f"❌ No .proto files found in {proto_root}")
        return

    print(f"✅ Found {len(proto_files)} proto files:")
    for f in proto_files:
        print(f"   - {f.relative_to(proto_root)}")

    for output_dir in output_dirs:
        cmd = [
            "uv",
            "run",
            "python",
            "-m",
            "grpc_tools.protoc",
            f"-I{proto_root}",
            f"--python_out={output_dir}",
            f"--grpc_python_out={output_dir}",
            f"--pyi_out={output_dir}",  # ← Дополнительные .pyi от protobuf
            *[str(f) for f in proto_files],
        ]

        print(f"\n🚀 Running command:")
        print(" ".join(cmd))
        print("-" * 80)

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            print(
                f"\n✅ Successfully generated gRPC Python code with mypy types in:\n   {output_dir}"
            )
            print("   Generated files include .pyi stubs for better type hinting.")

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Generation failed with exit code {e.returncode}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            sys.exit(1)
        except FileNotFoundError as e:
            print(e)
            print("❌ Error: 'uv' command not found.")
            sys.exit(1)


if __name__ == "__main__":
    main()
