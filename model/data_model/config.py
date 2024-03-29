from pydantic import BaseModel


class User(BaseModel):
    role: str
    login: str
    password: str
    description: str
    space: str
    cookie: dict = {}


# @dataclass()
class Users(BaseModel):
    developer: User
    admin: User


class Timeouts(BaseModel):
    implicit_timeout: int
    cookie_expire: int


class Urls(BaseModel):
    base_url: str


class Defaults(BaseModel):
    password: str
    session: str


class Path(BaseModel):
    chromedriver_path: str


class Moon(BaseModel):
    user: str
    password: str
    host: str


# @dataclass
class StandConfig(BaseModel):
    urls: Urls
    timeouts: Timeouts
    users: Users
    defaults: Defaults
    paths: Path
    stand: str
    moon: Moon

    # # implicit_wait_timeout: int
    # # cookie_expire: int
    # chromedriver_path: str
    # developer: User
    # stand: str
    # default_password: str
