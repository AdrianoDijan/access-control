from pydantic import BaseModel


class LoginRequest(BaseModel):
    login: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
