import hashlib
import hmac
import json
import logging
import re
import msgspec
from settings import Settings
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi_sso import SSOBase
from pydantic import EmailStr
from shortuuid import encode as short_encode, decode as short_decode
from uuid import UUID, uuid4
import shortuuid
from typing import Literal
from urllib.parse import quote

from shared.redis import RedisService
from domain.session_service import SessionService
from shared.mail import MailSender
from loguru import logger

from stubs.user_stub import UserStub
from shared.contracts.user import (
    CreateUserRequest,
    GetUserByEmailRequest,
    LeagueAccount,
    UpdateUserRequest,
)


class AuthService:
    def __init__(
        self,
        ss: SessionService,
        mail_service: MailSender,
        redis_service: RedisService,
        settings: Settings,
        sso_dict: dict[str, SSOBase],
        user_stub: UserStub,
    ):

        self.session_service = ss
        self.SECRET_KEY = settings.secret_key
        self.sso_dict = sso_dict
        self.redis = redis_service
        self.mail_serive = mail_service
        self.user_stub = user_stub

    def sign_session(self, session_id: UUID) -> str:

        enc = short_encode(session_id)

        signature = hmac.new(
            self.SECRET_KEY.encode(), str(session_id).encode(), hashlib.sha256
        ).hexdigest()

        return f"{enc}.{signature}"

    def verify_session(self, signed_id: str) -> UUID | None:
        try:
            session_id_enc, signature = signed_id.rsplit(".", 1)

            session_id = short_decode(session_id_enc)

            expected_signature = hmac.new(
                self.SECRET_KEY.encode(),
                str(session_id).encode(),
                hashlib.sha256,
            ).hexdigest()

            if hmac.compare_digest(signature, expected_signature):
                return session_id

        except (ValueError, AttributeError, KeyError) as e:
            print(f"Verification error: {e}")
            return None

    def get_sso(self, sso: Literal["yandex", "discord"]):
        if sso != "email":
            return self.sso_dict.get(sso)

    async def init_verify_user_email(self, email: EmailStr):
        ver_ses_id = uuid4()
        code = shortuuid.ShortUUID().random(length=6)
        await self.redis.create(key=f"cvid:{str(ver_ses_id)}", value=code, ttl=10 * 60)
        self.mail_serive.send_email(email, "Code verification", str(code))

        from fastapi.responses import JSONResponse

        response = JSONResponse(content={"message": "code_sent"})

        response.set_cookie(
            key="email",
            value=email,
            httponly=True,
            samesite="lax",
            max_age=30 * 24 * 60 * 60,
        )

        response.set_cookie(
            key="cvid",
            value=str(ver_ses_id),
            httponly=True,
            samesite="lax",
            max_age=30 * 24 * 60 * 60,
        )
        return response

    async def init_desktop_email_login(self, email: EmailStr):
        verification_id = uuid4()
        code = shortuuid.ShortUUID().random(length=6)
        await self.redis.create(
            key=f"desktop:cvid:{str(verification_id)}",
            value={"email": str(email), "code": code},
            ttl=10 * 60,
        )
        self.mail_serive.send_email(email, "Code verification", str(code))
        return {"message": "code_sent", "verification_id": str(verification_id)}

    async def finish_verify_user_email(self, email: EmailStr, cvid: str, code: str):

        req_code = await self.redis.get(f"cvid:{cvid}")

        if req_code == code:
            return await self.register_user(email, "email", return_json=True)

        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Invalid verification code")

    async def finish_desktop_email_login(self, verification_id: str, code: str):
        from fastapi import HTTPException

        try:
            data = await self.redis.get(f"desktop:cvid:{verification_id}")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid verification session")

        if data.get("code") != code:
            raise HTTPException(status_code=401, detail="Invalid verification code")

        signed_sid, user = await self.create_user_session(
            data["email"], "desktop_email"
        )
        await self.redis.delete(f"desktop:cvid:{verification_id}")
        return {"authenticated": True, "sid": signed_sid, "user": user}

    async def verify_user_oauth(
        self, provider: Literal["yandex", "discord"], request: Request
    ):

        async with self.get_sso(provider) as sso:
            logger.info("init sso")

            user = await sso.verify_and_process(request)

            if user:
                return await self.register_user(user.email, user.provider)
        return RedirectResponse(url="/auth-error")

    async def create_user_session(self, email, provider):
        user_data = None
        try:
            user_data = await self.user_stub.get_user_by_email(
                GetUserByEmailRequest(email=email)
            )
        except Exception as e:
            logger.warning(f"User not found, creating new user: {e}")
            try:
                user_data = await self.user_stub.create_user(
                    CreateUserRequest(email=email)
                )
            except Exception as create_e:
                logger.error(f"Failed to create user: {create_e}")
                from fastapi import HTTPException

                raise HTTPException(status_code=500, detail="Failed to create user")

        data = user_data.model_dump() if user_data else None
        ses_id = uuid4()
        signed_ses = self.sign_session(ses_id)
        ses_id = await self.session_service.create_session(
            ses_id=ses_id,
            email=email,
            provider=provider,
            user_data=data,
            sign=signed_ses,
        )
        for k, v in data.items():
            if "id" in k.lower():
                data[k] = str(data[k])
        return signed_ses, data

    async def register_user(self, email, provider, return_json=False):
        signed_ses, data = await self.create_user_session(email, provider)
        if return_json:
            from fastapi.responses import JSONResponse

            response = JSONResponse(content={"authenticated": True, "user": data})
        else:
            response = RedirectResponse(url="https://akiora.webhop.me/about")

        response.set_cookie(
            key="sid",
            value=signed_ses,
            httponly=True,
            samesite="lax",
            max_age=30 * 24 * 60 * 60,
            path="/",
        )

        return response

    async def start_lol_account_verification(
        self,
        signed_sid: str,
        server: str,
        username: str,
        tagline: str,
    ):
        from fastapi import HTTPException

        if self.verify_session(signed_sid) is None:
            raise HTTPException(status_code=401, detail="Invalid session")

        riot_id = f"{username}#{tagline}"
        payload = await self._fetch_opgg_summoner(server, riot_id)
        summoner = self._first_opgg_summoner(payload)
        if not summoner:
            raise HTTPException(status_code=404, detail="Summoner not found")

        profile_image_url = summoner.get("profile_image_url")
        current_profile_icon_id = self._parse_profile_icon_id(profile_image_url)
        if current_profile_icon_id is None:
            raise HTTPException(
                status_code=502, detail="Profile icon is missing in OP.GG response"
            )

        target_icon_id = current_profile_icon_id % 30 + 1
        target_profile_image_url = self._replace_profile_icon_id(
            profile_image_url, target_icon_id
        )
        solo_tier_info = summoner.get("solo_tier_info") or {}
        verification_id = uuid4()
        await self.redis.create(
            key=f"lol:cvid:{str(verification_id)}",
            value={
                "sid": signed_sid,
                "server": server.lower(),
                "username": summoner.get("game_name") or username,
                "tagline": summoner.get("tagline") or tagline,
                "current_profile_icon_id": current_profile_icon_id,
                "target_icon_id": target_icon_id,
                "profile_image_url": profile_image_url,
                "target_profile_image_url": target_profile_image_url,
                "solo_tier": solo_tier_info.get("tier"),
                "solo_division": solo_tier_info.get("division"),
                "solo_lp": solo_tier_info.get("lp"),
                "solo_tier_image_url": solo_tier_info.get("tier_image_url"),
            },
            ttl=10 * 60,
        )
        return {
            "verification_id": str(verification_id),
            "current_profile_icon_id": current_profile_icon_id,
            "profile_image_url": profile_image_url,
            "target_icon_id": target_icon_id,
            "target_profile_image_url": target_profile_image_url,
            "solo_tier": solo_tier_info.get("tier"),
            "solo_division": solo_tier_info.get("division"),
            "solo_lp": solo_tier_info.get("lp"),
            "solo_tier_image_url": solo_tier_info.get("tier_image_url"),
            "server": server.lower(),
            "riot_id": f"{summoner.get('game_name') or username}#{summoner.get('tagline') or tagline}",
        }

    async def finish_lol_account_verification(
        self, signed_sid: str, verification_id: str
    ):
        from fastapi import HTTPException
        import httpx

        if self.verify_session(signed_sid) is None:
            raise HTTPException(status_code=401, detail="Invalid session")

        try:
            challenge = await self.redis.get(f"lol:cvid:{verification_id}")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid verification session")

        if challenge.get("sid") != signed_sid:
            raise HTTPException(
                status_code=403, detail="Verification belongs to another session"
            )

        payload = await self._fetch_opgg_summoner(
            challenge["server"],
            f"{challenge['username']}#{challenge['tagline']}",
        )
        actual_icon_id = self._extract_profile_icon_id(payload)
        if actual_icon_id != int(challenge["target_icon_id"]):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Profile icon is not changed yet",
                    "expected_icon_id": challenge["target_icon_id"],
                    "actual_icon_id": actual_icon_id,
                },
            )

        summoner = self._first_opgg_summoner(payload) or {}
        solo_tier_info = summoner.get("solo_tier_info") or {}

        session = await self.session_service.get_session(signed_sid)
        user_data = session.custom_data.get("user") if session else None
        if not user_data or not user_data.get("id"):
            raise HTTPException(status_code=401, detail="Session user is missing")

        existing_accounts = [
            LeagueAccount(**account)
            for account in user_data.get("league_accounts", [])
            if not (
                account.get("server") == challenge["server"]
                and account.get("username") == challenge["username"]
                and account.get("tagline") == challenge["tagline"]
            )
        ]
        existing_accounts.append(
            LeagueAccount(
                status="done",
                username=challenge["username"],
                tagline=challenge["tagline"],
                server=challenge["server"],
                profile_image_url=summoner.get("profile_image_url")
                or challenge.get("target_profile_image_url")
                or challenge.get("profile_image_url"),
                solo_tier=solo_tier_info.get("tier") or challenge.get("solo_tier"),
                solo_division=solo_tier_info.get("division")
                or challenge.get("solo_division"),
                solo_lp=solo_tier_info.get("lp") or challenge.get("solo_lp"),
                solo_tier_image_url=solo_tier_info.get("tier_image_url")
                or challenge.get("solo_tier_image_url"),
            )
        )

        updated_user = await self.user_stub.update_user(
            UpdateUserRequest(
                user_id=UUID(user_data["id"]),
                league_accounts=existing_accounts,
            )
        )
        updated_user_data = updated_user.model_dump()
        for k, v in updated_user_data.items():
            if "id" in k.lower():
                updated_user_data[k] = str(v)
        if session:
            session.custom_data["user"] = updated_user_data
            await self.session_service.repo.create(signed_sid, session)
        await self.redis.delete(f"lol:cvid:{verification_id}")
        return {
            "verified": True,
            "profile_icon_id": actual_icon_id,
            "user": updated_user_data,
        }

    async def _fetch_opgg_summoner(self, server: str, riot_id: str):
        from fastapi import HTTPException
        import httpx

        url = (
            f"https://lol-api-summoner.op.gg/api/v3/{server.lower()}/summoners"
            f"?riot_id={quote(riot_id)}&hl=en_US"
        )
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
        if response.status_code >= 400:
            raise HTTPException(
                status_code=502, detail="Failed to fetch OP.GG summoner"
            )
        return response.json()

    def _first_opgg_summoner(self, payload):
        data = payload.get("data") if isinstance(payload, dict) else None
        if isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict):
                return first
        return None

    def _extract_profile_icon_id(self, payload) -> int | None:
        icon_keys = {
            "profile_icon_id",
            "profileIconId",
            "profile_image_id",
            "profileImageId",
            "icon_id",
            "iconId",
        }

        def walk(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key in icon_keys and isinstance(item, int):
                        return item
                    if (
                        isinstance(item, str)
                        and "profile" in key.lower()
                        and ("icon" in key.lower() or "image" in key.lower())
                    ):
                        match = re.search(r"(\d+)(?:\.\w+)?$", item)
                        if match:
                            return int(match.group(1))
                    found = walk(item)
                    if found is not None:
                        return found
            if isinstance(value, list):
                for item in value:
                    found = walk(item)
                    if found is not None:
                        return found
            return None

        return walk(payload)

    def _parse_profile_icon_id(self, profile_image_url: str | None) -> int | None:
        if not profile_image_url:
            return None
        last_part = profile_image_url.rsplit("/", 1)[-1]
        match = re.search(r"profileIcon(\d+)", last_part)
        if match:
            return int(match.group(1))
        fallback = re.search(r"(\d+)", last_part)
        return int(fallback.group(1)) if fallback else None

    def _replace_profile_icon_id(
        self, profile_image_url: str | None, icon_id: int
    ) -> str | None:
        if not profile_image_url:
            return None
        return re.sub(r"profileIcon\d+", f"profileIcon{icon_id}", profile_image_url)

    async def verify_session_handler(self, msg: dict):
        signed_sid = msg.get("sid")
        id = self.verify_session(signed_sid)

        if id:
            ses = await self.session_service.get_session(id)
            return ses.model_dump()

        return None
