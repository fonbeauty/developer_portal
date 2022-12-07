from dataclasses import dataclass


@dataclass()
class User:
    login: str
    password: str
    description: str
    session: str
    space: str


@dataclass
class StandConfig:
    base_url: str
    implicit_wait_timeout: int
    cookie_expire: int
    chromedriver_path: str
    developer: User
    stand: str
    default_password: str
