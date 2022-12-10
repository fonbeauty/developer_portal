import yaml

from pathlib import Path
from pydantic import ValidationError

from model.models import StandConfig


def load_yml_data(path: str) -> dict:
    with open(path, 'r', encoding='utf8') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f'ERROR {exc}')
            raise exc


def get_config(stand: str) -> StandConfig:
    ymlconfig = load_yml_data(f'{str(Path(__file__).parent.parent)}/configs/{stand}_config.yml')
    ymlconfig['stand'] = stand
    stand_config = ''
    try:
        stand_config = StandConfig.parse_obj(ymlconfig)
    except ValidationError as e:
        print(e)
    return stand_config
