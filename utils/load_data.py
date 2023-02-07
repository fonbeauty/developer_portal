import logging
import yaml

from pathlib import Path
from pydantic import ValidationError

from model.data_model.config import StandConfig
from model.data_model.test_data import TestData

LOGGER = logging.getLogger(__name__)


def _load_yml_data(path: str) -> dict:
    with open(path, 'r', encoding='utf8') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f'ERROR {exc}')
            raise exc


def get_config(stand: str) -> StandConfig:
    ymlconfig = _load_yml_data(f'{str(Path(__file__).parent.parent)}/configs/{stand}_config.yml')
    ymlconfig['stand'] = stand
    stand_config = ''
    try:
        stand_config = StandConfig.parse_obj(ymlconfig)
    except ValidationError as e:
        LOGGER.exception('Ошибка загрузки конфига')
        raise e
    return stand_config


def get_test_data(stand: str) -> TestData:
    ymlconfig = _load_yml_data(f'{str(Path(__file__).parent.parent)}/configs/{stand}_test_data.yml')
    test_data = ''
    try:
        test_data = TestData.parse_obj(ymlconfig)
    except ValidationError as e:
        LOGGER.exception('Ошибка загрузки тестовых данных')
        raise e
    return test_data
