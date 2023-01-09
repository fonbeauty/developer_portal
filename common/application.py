import logging
import uuid

from bs4 import BeautifulSoup

from common.sessions import PortalSession
from model.models import StandConfig

LOGGER = logging.getLogger(__name__)


class Application:

    def __init__(self,
                 config: StandConfig,
                 app_href: str = '',
                 password: str = None,
                 description: str = 'Приложение создано автотестами, можно удалить'
                                    ' Application was created by autotests, it may be deleted',
                 name: str = f"autotest_{uuid.uuid4()}",
                 ):
        self.CONFIG = config
        self.password = password or config.defaults.password
        self.app_description = description
        self.app_name = name
        self.app_href = app_href

    def create(self, session: PortalSession):
        with session as s:
            response = s.get(
                url=f'{self.CONFIG.urls.base_url}/profile/{self.CONFIG.users.developer.space}/app/create'
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            form_build_id = soup.select('input[name=form_build_id]')[0]['value']
            form_token = soup.select('input[name=form_token]')[0]['value']

            request_body = {
                'app_name': f'autotest_{uuid.uuid4()}',
                'app_description': 'Приложение создано автотестами, можно удалить'
                                   'Application was created by autotests, it may be deleted',
                'oauth[]': '',
                'password': self.password,
                'password_confirm': self.password,
                'form_build_id': f'{form_build_id}',
                'form_token': f'{form_token}',
                'form_id': 'application_create_download_cert_form',
                'save': 'создать'
            }

            response = s.post(
                url=f'{self.CONFIG.urls.base_url}/profile/{self.CONFIG.users.developer.space}/app/create',
                data=request_body
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            self.app_href = f'{self.CONFIG.urls.base_url}{soup.select("#edit-to-app")[0]["href"]}'
            LOGGER.info(f'Создано приложение {self.app_href}')
        return self

    def delete(self, session: PortalSession):
        with session as s:
            response = s.get(
                url=f'{self.app_href}/delete'
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            form_build_id = soup.select('input[name=form_build_id]')[0]['value']
            form_token = soup.select('input[name=form_token]')[0]['value']

            request_body = {
                # 'op': 'да, хочу',
                # 'confirm': 1,
                'form_build_id': f'{form_build_id}',
                'form_token': f'{form_token}',
                'form_id': 'application_delete'
            }

            delete_response = s.post(
                url=f'{self.app_href}/delete',
                data=request_body
            )
            delete_response.raise_for_status()
            LOGGER.info(f'Приложение удалено {self.app_href}')
        return self
