from typing import Literal, Annotated
from fastapi import APIRouter, Request, Cookie, Header, HTTPException

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from domain.auth_service import AuthService
from domain.session_service import SessionService
from loguru import logger


class CookieSchema(BaseModel):
    sid: str | None = None
    cvid: str | None = None
    email: EmailStr | None = None
    model_config = ConfigDict(extra="ignore")


class LoginInitRequest(BaseModel):
    email: EmailStr


class LoginFInishRequest(BaseModel):
    code: str = Field(..., max_length=6, min_length=6)


class DesktopLoginFinishRequest(BaseModel):
    verification_id: str
    code: str = Field(..., max_length=6, min_length=6)


class LolVerificationStartRequest(BaseModel):
    server: str = Field(..., min_length=2, max_length=8)
    username: str = Field(..., min_length=1, max_length=32)
    tagline: str = Field(..., min_length=1, max_length=16)


class LolVerificationFinishRequest(BaseModel):
    verification_id: str


class AuthResponse(BaseModel):
    user: dict
    authenticated: bool


router = APIRouter(route_class=DishkaRoute)

ProviderType = Literal[
    "yandex",
    "discord",
]


def _session_token(cookie: CookieSchema, authorization: str | None) -> str:
    if cookie.sid:
        return cookie.sid
    if authorization:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer" and token:
            return token
    raise HTTPException(status_code=401, detail="Missing session")


@router.post("/logout")
async def logout(
    cookie: Annotated[CookieSchema, Cookie()],
    auth_service: FromDishka[AuthService],
    session_service: FromDishka[SessionService],
):
    from fastapi.responses import JSONResponse

    response = JSONResponse(content={"message": "logged_out"})
    response.delete_cookie(key="sid", path="/", domain="localhost")
    response.delete_cookie(key="email", path="/", domain="localhost")
    response.delete_cookie(key="cvid", path="/", domain="localhost")

    if cookie.sid:
        session_id = auth_service.verify_session(cookie.sid)
        if session_id:
            await session_service.delete_session(session_id)

    return response


@router.get("/me", response_model=AuthResponse)
async def me(
    cookie: Annotated[CookieSchema, Cookie()],
    auth_service: FromDishka[AuthService],
    session_service: FromDishka[SessionService],
):
    if not cookie.sid:
        raise HTTPException(status_code=401)
    ssid = cookie.sid
    logger.info(f"Session ID from cookie: {ssid}")
    sid = auth_service.verify_session(ssid)
    logger.info(f"Verified Session ID: {sid}")
    if data := await session_service.get_session_user(ssid):
        logger.info(f"User data from session: {data}")
        return {"authenticated": True, "user": data}
    raise HTTPException(status_code=404)


@router.get("/{provider}/login")
async def login_oauth(provider: ProviderType, auth_service: FromDishka[AuthService]):

    async with auth_service.get_sso(provider) as sso:
        return await sso.get_login_redirect()


@router.get("/auth/{provider}/callback")
async def auth_callback(
    provider: ProviderType, request: Request, auth_service: FromDishka[AuthService]
):
    return await auth_service.verify_user_oauth(provider, request)


@router.post("/email/login/start")
async def login_email(
    req_body: LoginInitRequest, auth_service: FromDishka[AuthService]
):
    return await auth_service.init_verify_user_email(req_body.email)


@router.post("/email/login/finish")
async def enter_email_code(
    req_body: LoginFInishRequest,
    cookie: Annotated[CookieSchema, Cookie()],
    auth_service: FromDishka[AuthService],
):

    return await auth_service.finish_verify_user_email(
        cookie.email, cookie.cvid, req_body.code
    )


@router.post("/desktop/email/login/start")
async def desktop_login_email(
    req_body: LoginInitRequest, auth_service: FromDishka[AuthService]
):
    return await auth_service.init_desktop_email_login(req_body.email)


@router.post("/desktop/email/login/finish")
async def desktop_enter_email_code(
    req_body: DesktopLoginFinishRequest,
    auth_service: FromDishka[AuthService],
):
    return await auth_service.finish_desktop_email_login(
        req_body.verification_id, req_body.code
    )


@router.post("/lol/verification/start")
async def start_lol_verification(
    req_body: LolVerificationStartRequest,
    cookie: Annotated[CookieSchema, Cookie()],
    auth_service: FromDishka[AuthService],
    authorization: str | None = Header(default=None),
):
    return await auth_service.start_lol_account_verification(
        _session_token(cookie, authorization),
        req_body.server,
        req_body.username,
        req_body.tagline,
    )


@router.post("/lol/verification/finish")
async def finish_lol_verification(
    req_body: LolVerificationFinishRequest,
    cookie: Annotated[CookieSchema, Cookie()],
    auth_service: FromDishka[AuthService],
    authorization: str | None = Header(default=None),
):
    return await auth_service.finish_lol_account_verification(
        _session_token(cookie, authorization), req_body.verification_id
    )
