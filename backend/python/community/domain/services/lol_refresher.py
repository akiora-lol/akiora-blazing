"""Periodic LoL account refresher.

Iterates over all users with verified League accounts and re-fetches their
profile icon, rank, and tier image via the OP.GG public summoner endpoint
(the same endpoint used by auth_service during verification).
"""

import asyncio
import re
from datetime import datetime, UTC
from urllib.parse import quote

import httpx
from loguru import logger

from domain.entites.user import User, LeagueAccount


OPGG_URL_TEMPLATE = (
    "https://lol-api-summoner.op.gg/api/v3/{server}/summoners"
    "?riot_id={riot_id}&hl=en_US"
)


class LolRefresher:
    """Periodically refresh users' LeagueAccount data from OP.GG.

    Runs as a background asyncio task. Iterates the user collection in
    batches, looks up each verified account, and merges the latest rank /
    profile icon back into the user document.
    """

    def __init__(
        self,
        *,
        interval_seconds: int = 30 * 60,
        batch_size: int = 50,
        per_request_concurrency: int = 4,
        request_timeout: float = 10.0,
        inter_user_delay: float = 0.25,
    ):
        self.interval_seconds = interval_seconds
        self.batch_size = batch_size
        self.per_request_concurrency = per_request_concurrency
        self.request_timeout = request_timeout
        self.inter_user_delay = inter_user_delay
        self._task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()

    def start(self) -> None:
        if self._task is not None:
            return
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run(), name="lol-refresher")
        logger.info(
            "LolRefresher started: interval={}s batch={} concurrency={}",
            self.interval_seconds,
            self.batch_size,
            self.per_request_concurrency,
        )

    async def stop(self) -> None:
        if self._task is None:
            return
        self._stop_event.set()
        self._task.cancel()
        try:
            await self._task
        except (asyncio.CancelledError, Exception):
            pass
        self._task = None
        logger.info("LolRefresher stopped")

    async def _run(self) -> None:
        # Stagger first run a bit so the gRPC server can fully come up.
        try:
            await asyncio.wait_for(self._stop_event.wait(), timeout=30)
            return
        except asyncio.TimeoutError:
            pass

        while not self._stop_event.is_set():
            started = datetime.now(UTC)
            try:
                processed = await self._refresh_once()
                logger.info(
                    "LolRefresher cycle done: users_processed={} took={:.1f}s",
                    processed,
                    (datetime.now(UTC) - started).total_seconds(),
                )
            except Exception as exc:  # never let the loop die
                logger.exception("LolRefresher cycle failed: {}", exc)

            try:
                await asyncio.wait_for(
                    self._stop_event.wait(), timeout=self.interval_seconds
                )
                return  # stop requested
            except asyncio.TimeoutError:
                continue

    async def _refresh_once(self) -> int:
        processed = 0
        sem = asyncio.Semaphore(self.per_request_concurrency)
        async with httpx.AsyncClient(timeout=self.request_timeout) as client:
            # Iterate the whole collection lazily so we don't blow up memory.
            cursor = User.find(
                {"league_accounts": {"$exists": True, "$ne": None}}
            )
            async for user in cursor:
                if self._stop_event.is_set():
                    break
                if not user.league_accounts:
                    continue

                async def _bounded_refresh(account: LeagueAccount) -> LeagueAccount:
                    async with sem:
                        return await self._refresh_account(client, account)

                refreshed = await asyncio.gather(
                    *[_bounded_refresh(account) for account in user.league_accounts],
                    return_exceptions=False,
                )

                changed = any(
                    self._account_changed(before, after)
                    for before, after in zip(user.league_accounts, refreshed)
                )
                if changed:
                    user.league_accounts = refreshed
                    user.last_updated = datetime.now(UTC)
                    try:
                        await user.save()
                    except Exception as exc:
                        logger.warning(
                            "Failed to persist refreshed LoL data for user {}: {}",
                            user.id,
                            exc,
                        )

                processed += 1
                if self.inter_user_delay:
                    await asyncio.sleep(self.inter_user_delay)
        return processed

    async def _refresh_account(
        self, client: httpx.AsyncClient, account: LeagueAccount
    ) -> LeagueAccount:
        # Only refresh verified accounts; pending ones haven't completed
        # the icon-change challenge yet, so nothing to refresh.
        if account.status != "done":
            return account
        if not account.username or not account.tagline or not account.server:
            return account
        try:
            payload = await self._fetch_opgg_summoner(
                client, account.server, f"{account.username}#{account.tagline}"
            )
        except Exception as exc:
            logger.debug(
                "OP.GG fetch failed for {}#{} ({}): {}",
                account.username,
                account.tagline,
                account.server,
                exc,
            )
            return account

        summoner = self._first_opgg_summoner(payload) or {}
        solo_tier_info = summoner.get("solo_tier_info") or {}

        return LeagueAccount(
            status="done",
            username=account.username,
            tagline=account.tagline,
            server=account.server,
            profile_image_url=summoner.get("profile_image_url") or account.profile_image_url,
            solo_tier=solo_tier_info.get("tier") or account.solo_tier,
            solo_division=solo_tier_info.get("division") or account.solo_division,
            solo_lp=solo_tier_info.get("lp") if solo_tier_info.get("lp") is not None else account.solo_lp,
            solo_tier_image_url=solo_tier_info.get("tier_image_url") or account.solo_tier_image_url,
        )

    @staticmethod
    async def _fetch_opgg_summoner(
        client: httpx.AsyncClient, server: str, riot_id: str
    ) -> dict:
        url = OPGG_URL_TEMPLATE.format(server=server.lower(), riot_id=quote(riot_id))
        response = await client.get(url)
        if response.status_code >= 400:
            raise RuntimeError(f"OP.GG returned {response.status_code}")
        return response.json()

    @staticmethod
    def _first_opgg_summoner(payload):
        data = payload.get("data") if isinstance(payload, dict) else None
        if isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict):
                return first
        return None

    @staticmethod
    def _account_changed(before: LeagueAccount, after: LeagueAccount) -> bool:
        return (
            before.profile_image_url != after.profile_image_url
            or before.solo_tier != after.solo_tier
            or before.solo_division != after.solo_division
            or before.solo_lp != after.solo_lp
            or before.solo_tier_image_url != after.solo_tier_image_url
        )
