from common.sessions import BaseSession
from model.models import StandConfig


def get_logs(session: BaseSession, config: StandConfig):
    with session as s:
        response = s.get(f'{config.urls.base_url}/admin/sbt/request-log/json')
        log = response.json()
        return log
