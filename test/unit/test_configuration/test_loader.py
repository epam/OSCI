import pytest
from osci.config.reader import BaseYmlConfigReader, BaseConfigReader


def test_base_config_abstract___read():
    with pytest.raises(NotImplementedError):
        BaseConfigReader(env='test').read()


def test_abstract_base_config___check_exists():
    with pytest.raises(NotImplementedError):
        BaseConfigReader(env='test').exists()


def test_base_yaml__check_exists():
    assert BaseYmlConfigReader(env='test').exists()


def test_base_yaml__read():
    assert isinstance(BaseYmlConfigReader(env='test').read(), dict)

