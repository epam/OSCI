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

import logging
import os

from typing import Dict, Union
from .reader import BaseYmlConfigReader

log = logging.getLogger(__name__)


class MetaSingleton(type):
    """Metaclass for create singleton"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
            log.debug(f'Create new {cls}')
        return cls._instances[cls]


class BaseConfig(metaclass=MetaSingleton):
    """Abstract class for all configurations"""

    @classmethod
    def tear_down(cls):
        """Delete all instances of the class"""
        cls._instances = {}
        log.debug(f'Delete all instances of {cls}')


class Config(BaseConfig):
    """Configuration is a Singleton and will be using just one configuration instance

    Priorities of how to get the configuration:
        1. Passed env during initialization of the class
        2. Environment variable `ENV`
        4. Using `local.yml` config if exists
        3. Using `default.yml` config
    """

    def __init__(self, env: str = None):
        """Init configuration

        :param env: environment on which the database configuration should be obtained
        """
        self.env = env or os.environ.get('ENV') or ('local'
                                                    if BaseYmlConfigReader.check_exists(env='local')
                                                    else None) or 'default'
        self.__cfg = BaseYmlConfigReader.read(self.env)
        log.info(f'Configuration loaded for env:{self.env}')

    @property
    def database_connection_string(self) -> str:
        """Get pyodbc connection string

        :return: connection string
        """
        return "Driver={{driver}};Server={host};Port={port};UID={user};PWD={password};".format(**self.database)

    @property
    def database(self) -> Dict[str, Union[str, int]]:
        """Retrieve database configs"""
        return self['db']

    def __getitem__(self, key):
        """Get item from configuration dict

        :param key: key
        :return: item
        """
        return self.__cfg[key]
