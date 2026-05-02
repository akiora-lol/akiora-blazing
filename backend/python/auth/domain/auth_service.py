import hashlib
import hmac
import json
import logging
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

from shared.redis import RedisService
from domain.session_service import SessionService
from shared.mail import MailSender
from loguru import logger

from stubs.user_stub import UserStub
from shared.contracts.user import GetUserByEmailRequest, CreateUserRequest


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
            domain="localhost",
            httponly=True,
            samesite="lax",
            max_age=30 * 24 * 60 * 60,
        )

        response.set_cookie(
            key="cvid",
            value=str(ver_ses_id),
            httponly=True,
            domain="localhost",
            samesite="lax",
            max_age=30 * 24 * 60 * 60,
        )
        return response

    async def finish_verify_user_email(self, email: EmailStr, cvid: str, code: str):

        req_code = await self.redis.get(f"cvid:{cvid}")

        if req_code == code:
            return await self.register_user(email, "email", return_json=True)

        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Invalid verification code")

    async def verify_user_oauth(
        self, provider: Literal["yandex", "discord"], request: Request
    ):

        async with self.get_sso(provider) as sso:
            logger.info("init sso")

            user = await sso.verify_and_process(request)

            if user:
                return await self.register_user(user.email, user.provider)
        return RedirectResponse(url="/auth-error")

    async def register_user(self, email, provider, return_json=False):
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
                if return_json:
                    from fastapi import HTTPException

                    raise HTTPException(status_code=500, detail="Failed to create user")
                return RedirectResponse(url="/auth-error")

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
        if return_json:
            from fastapi.responses import JSONResponse

            response = JSONResponse(content={"authenticated": True, "user": data})
        else:
            response = RedirectResponse(url="http://localhost:3000/about")

        response.set_cookie(
            key="sid",
            value=signed_ses,
            httponly=True,
            samesite="lax",
            max_age=30 * 24 * 60 * 60,
            path="/",
            domain="localhost",
        )

        return response

    async def verify_session_handler(self, msg: dict):
        signed_sid = msg.get("sid")
        id = self.verify_session(signed_sid)

        if id:
            ses = await self.session_service.get_session(id)
            return ses.model_dump()

        return None
