from sqlmodel import SQLModel


class AuthRequest(SQLModel):
    username: str


class AuthResponse(SQLModel):
    valid: bool
    message: str