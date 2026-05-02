from pydantic import BaseModel, ConfigDict, EmailStr


class CookieSchema(BaseModel):
    sid: str | None = None
    cvid: str | None = None
    email: EmailStr | None = None
    model_config = ConfigDict(extra="ignore")
