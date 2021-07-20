from osci.config import Config


def test_config_singleton():
    config1 = Config()
    config2 = Config()
    Config.tear_down()
    assert id(config1) == id(config2)
