from typing import Literal, Annotated
from fastapi import APIRouter, Request, Cookie, HTTPException

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


class AuthResponse(BaseModel):
    user: dict
    authenticated: bool


router = APIRouter(route_class=DishkaRoute)

ProviderType = Literal[
    "yandex",
    "discord",
]


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
