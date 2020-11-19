import pytest
from __app__.datalake.config.reader import BaseYmlConfigReader, BaseConfigReader


def test_base_config_abstract___read():
    with pytest.raises(NotImplementedError):
        BaseConfigReader().read(env='test')


def test_abstract_base_config___check_exists():
    with pytest.raises(NotImplementedError):
        BaseConfigReader().check_exists(env='test')


def test_base_yaml__check_exists():
    assert BaseYmlConfigReader().check_exists(env='test')


def test_base_yaml__read():
    assert isinstance(BaseYmlConfigReader().read(env='test'), dict)

