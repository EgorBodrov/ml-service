from pydantic import BaseModel


class SignUpUserRequest(BaseModel):
    name: str
    email: str
    password: str


class SignUpUserResponse(BaseModel):
    name: str
    email: str


class SignInUserRequest(BaseModel):
    email: str
    password: str


class SignInUserResponse(BaseModel):
    name: str
    email: str
    token: str
    token_type: str = "Bearer"
