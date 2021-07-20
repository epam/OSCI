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

from typing import Dict, Any, Union, Callable, Optional
from pathlib import Path
from deepmerge import always_merger

import logging
import yaml
import os

log = logging.getLogger(__name__)

META_CONFIG_FIELD = 'meta'
CONFIG_SOURCE_TYPE_FIELD = 'config_source'
CONFIG_SOURCE_TYPE_ENV = 'env'
CONFIG_SOURCE_TYPE_DATABRICKS = 'dbutils'
DATABRICKS_SECRETS_SCOPE_FIELD = 'databricks_scope'
PARENT_CONFIG_FIELD = 'extends'


class BaseConfigReader:
    """Abstract class for all configurations reader"""

    def __init__(self, env: str, *args, **kwargs):
        self.env = env
        self.__cfg: Optional[Dict[str, Any]] = None

    def read(self) -> Dict[str, Any]:
        """Read config by environment key"""
        raise NotImplementedError()

    @property
    def config(self):
        if self.__cfg is None:
            return self.read()
        return self.__cfg

    @config.setter
    def config(self, cfg):
        self.__cfg = cfg

    def exists(self) -> bool:
        """Check configuration exists"""
        raise NotImplementedError()


def read_config_from_databricks_secrets(config: dict, dbutils=None) -> dict:
    log.debug('Check read config from databricks secrets variables')
    out_config = dict()
    if dbutils is None:
        log.error('`dbutils` is not defined')
        return out_config
    try:
        scope = config[META_CONFIG_FIELD][DATABRICKS_SECRETS_SCOPE_FIELD]

        def _load_variables_from_secrets(variable):
            if isinstance(variable, dict):
                return {
                    k: _load_variables_from_secrets(v) for k, v in variable.items()
                }
            if isinstance(variable, list):
                return [_load_variables_from_secrets(v) for v in variable]
            return dbutils.secrets.get(scope=scope, key=str(variable))

        out_config = {k: _load_variables_from_secrets(v) for k, v in config.items() if k != META_CONFIG_FIELD}
    except KeyError as ex:
        log.error(f'Databricks scope field (`{DATABRICKS_SECRETS_SCOPE_FIELD}`) not found '
                  f'in {config[META_CONFIG_FIELD]}: {ex}')

    return out_config


def read_config_from_environ(config: dict, *args, **kwargs) -> dict:
    log.debug('Check read config from environ variables')

    def _load_variables_from_env(variable):
        if isinstance(variable, dict):
            return {
                k: _load_variables_from_env(v) for k, v in variable.items()
            }
        if isinstance(variable, list):
            return [_load_variables_from_env(v) for v in variable]
        print('key', variable, 'value', os.environ.get(str(variable)))
        return os.environ.get(str(variable))

    return {k: _load_variables_from_env(v) for k, v in config.items() if k != META_CONFIG_FIELD}


readers_types_map: Dict[str, Callable[[dict, Optional[Any]], dict]] = {
    CONFIG_SOURCE_TYPE_ENV: read_config_from_environ,
    CONFIG_SOURCE_TYPE_DATABRICKS: read_config_from_databricks_secrets
}


class BaseYmlConfigReader(BaseConfigReader):
    """YAML config file reader"""

    DEFAULT_DIRECTORY_NAME = 'files'
    DEFAULT_DIRECTORY_PATH = Path(__file__).parent.resolve() / DEFAULT_DIRECTORY_NAME
    DEFAULT_FILE_FORMAT = 'yml'

    def __init__(self, env: str, directory_path: Union[str, Path] = DEFAULT_DIRECTORY_PATH,
                 file_format: str = DEFAULT_FILE_FORMAT, dbutils=None):
        """
        :param env: environment key (ex. `local`, `dev`, `stage`, `prod`, etc)
        :param directory_path: path to config files dictionary
        :param file_format: config file format (default: `yml`)
        """
        super().__init__(env)
        self.directory_path = directory_path
        self.file_format = file_format
        self.dbutils = dbutils

    @property
    def file_path(self):
        return Path(self.directory_path) / f"{self.env}.{self.file_format}"

    def read(self) -> Dict[str, Any]:
        """Read configuration from file

        Read and parse yaml configuration file by rule: `<directory_path>/<env>.<file_format>`
        :return: configuration dictionary
        """
        try:
            log.debug(f'Read config from {self.file_path}')
            with open(self.file_path) as config_file:
                self.__cfg = yaml.load(config_file, Loader=yaml.FullLoader)
                log.debug(f"Prod yml load: {self.__cfg}")
                meta = self.__cfg[META_CONFIG_FIELD].copy()
                if meta[CONFIG_SOURCE_TYPE_FIELD] in readers_types_map:
                    self.__cfg = readers_types_map[meta[CONFIG_SOURCE_TYPE_FIELD]](self.__cfg, self.dbutils)
                if meta.get(PARENT_CONFIG_FIELD) is not None:
                    self.__cfg = always_merger.merge(
                        BaseYmlConfigReader(env=meta.get(PARENT_CONFIG_FIELD),
                                            directory_path=self.directory_path,
                                            file_format=self.file_format).config,
                        self.__cfg
                    )
                log.debug(f"Prod yml res: {self.__cfg}")
                return self.__cfg
        except FileNotFoundError as ex:
            log.error(ex)
            raise ex

    def exists(self) -> bool:
        """Check configuration exists in `directory_path`
        :return: is exist file
        """
        log.debug(f'Check config file for env {self.env} exists')
        return self.file_path.is_file()
