from requests import Session
from requests.structures import CaseInsensitiveDict


class PortalSession(Session):

    def __init__(self, driver_cookie: dict):
        super().__init__()
        self.verify = False
        self.headers = CaseInsensitiveDict(
            {'Content-Type': 'application/x-www-form-urlencoded',
             'cookie': f'{driver_cookie["name"]}={driver_cookie["value"]}'}
        )
