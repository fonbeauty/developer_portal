import yaml

from pathlib import Path
from model.models import StandConfig, User


def load_yml_data(path: str) -> dict:
    with open(path, 'r', encoding='utf8') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f'ERROR {exc}')
            raise exc


def get_config(stand: str) -> StandConfig:
    ymlconfig = load_yml_data(f'{str(Path(__file__).parent.parent)}/configs/{stand}_config.yml')
    stand_config = StandConfig(
        base_url=f'{ymlconfig["urls"]["base_url"]}',
        implicit_wait_timeout=int(f'{ymlconfig["timeouts"]["implicit_timeout"]}'),
        cookie_expire=int(f'{ymlconfig["timeouts"]["cookie_expire"]}'),
        chromedriver_path=f'{ymlconfig["paths"]["chromedriver_path"]}',
        developer=User(
            login=ymlconfig["users"]["developer"]["login"],
            password=ymlconfig["users"]["developer"]["password"],
            description=ymlconfig["users"]["developer"]["description"],
            session=ymlconfig["users"]["developer"]["session"],
            space=ymlconfig["users"]["developer"]["space"],
        ),
        default_password=ymlconfig["default_password"]["create_application"],
        stand=stand
    )
    return stand_config
