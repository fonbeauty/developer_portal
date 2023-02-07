from pydantic import BaseModel


class User(BaseModel):
    role: str
    login: str
    password: str
    description: str
    space: str
    cookie: dict = {}


class Users(BaseModel):
    developer: User
    admin: User


class Defaults(BaseModel):
    password: str
    session: str


class TestData(BaseModel):
    users: Users
    defaults: Defaults
