"""Copyright since 2019, EPAM Systems

   This file is part of OSCI.

   OSCI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   OSCI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>."""

from typing import Dict, Any, Union
from pathlib import Path

import logging
import yaml
import os

log = logging.getLogger(__name__)

META_CONFIG_FIELD = 'meta'
CONFIG_SOURCE_TYPE_FIELD = 'config_source'
CONFIG_SOURCE_TYPE_ENV = 'env'


class BaseConfigReader:
    """Abstract class for all configurations reader"""

    @classmethod
    def read(cls, env: str, **kwargs) -> Dict[str, Any]:
        """Read config by environment key"""
        raise NotImplementedError()

    @classmethod
    def check_exists(cls, env: str, **kwargs) -> bool:
        """Check configuration exists"""
        raise NotImplementedError()


class BaseYmlConfigReader(BaseConfigReader):
    """YAML config file reader"""

    DEFAULT_DIRECTORY_NAME = 'files'
    DEFAULT_DIRECTORY_PATH = Path(__file__).parent.resolve() / DEFAULT_DIRECTORY_NAME
    DEFAULT_FILE_FORMAT = 'yml'

    @staticmethod
    def __file_path(filename: str, directory_path: Union[str, Path], file_format: str):
        return Path(directory_path) / f"{filename}.{file_format}"

    @classmethod
    def read(cls, env: str,
             directory_path: Union[str, Path] = DEFAULT_DIRECTORY_PATH,
             file_format: str = DEFAULT_FILE_FORMAT) -> Dict[str, Any]:
        """Read configuration from file

        Read and parse yaml configuration file by rule: `<directory_path>/<env>.<file_format>`

        :param env: environment key (ex. `local`, `dev`, `stage`, `prod`, etc)
        :param directory_path: path to config files dictionary
        :param file_format: config file format (default: `yml`)
        :return: configuration dictionary
        """
        try:
            file_path = cls.__file_path(filename=env,
                                        directory_path=directory_path,
                                        file_format=file_format)
            log.debug(f'Read config from {file_path}')
            with open(file_path) as config_file:
                cfg = yaml.load(config_file, Loader=yaml.FullLoader)
                if cfg[META_CONFIG_FIELD][CONFIG_SOURCE_TYPE_FIELD] == CONFIG_SOURCE_TYPE_ENV:
                    cfg = read_config_from_environ(config=cfg)
                return cfg
        except FileNotFoundError as ex:
            log.error(ex)
            raise ex

    @classmethod
    def check_exists(cls, env: str, directory_path: Union[str, Path] = DEFAULT_DIRECTORY_PATH,
                     file_format: str = DEFAULT_FILE_FORMAT) -> bool:
        """Check configuration exists in `directory_path`

        :param env: environment key (ex. `local`, `dev`, `stage`, `prod`, etc)
        :param directory_path: path to config files dictionary
        :param file_format: config file format (default: `yml`)
        :return: is exist file
        """
        log.debug(f'Check config file for env {env} exists')
        return cls.__file_path(filename=env, directory_path=directory_path, file_format=file_format).is_file()


def read_config_from_environ(config: dict) -> dict:
    log.debug('Check read config from environ variables')

    def _load_variables_from_env(variable):
        if isinstance(variable, dict):
            return {
                k: _load_variables_from_env(v) for k, v in variable.items()
            }
        if isinstance(variable, list):
            return [_load_variables_from_env(v) for v in variable]
        return os.environ.get(str(variable))

    return {
        **{META_CONFIG_FIELD: config[META_CONFIG_FIELD]},
        **{k: _load_variables_from_env(v) for k, v in config.items() if k != META_CONFIG_FIELD}
    }
