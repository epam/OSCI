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
import json

from typing import Mapping, Any, Dict, NamedTuple
from .reader import BaseYmlConfigReader
from osci.utils import MetaSingleton

log = logging.getLogger(__name__)


class BaseConfig(metaclass=MetaSingleton):
    """Abstract class for all configurations"""

    @classmethod
    def tear_down(cls):
        """Delete all instances of the class"""
        cls._instances = {}
        log.debug(f'Delete all instances of {cls}')


class FileSystemConfig(BaseConfig):

    def __init__(self, cfg):
        self.file_system_cfg = cfg.get('file_system', dict())
        self.areas_cfg = cfg.get('areas', dict())

    @property
    def landing_container(self) -> str:
        return self.areas_cfg.get('landing', dict()).get('container')

    @property
    def staging_container(self) -> str:
        return self.areas_cfg.get('staging', dict()).get('container')

    @property
    def public_container(self) -> str:
        return self.areas_cfg.get('public', dict()).get('container')

    @property
    def landing_props(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    def staging_props(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    def public_props(self) -> Dict[str, Any]:
        raise NotImplementedError()


class LocalFileSystemConfig(FileSystemConfig):
    @property
    def base_path(self) -> str:
        return self.file_system_cfg.get('base_path')

    @property
    def landing_props(self) -> Dict[str, Any]:
        return dict(base_path=self.base_path, base_area_dir=self.landing_container)

    @property
    def staging_props(self) -> Dict[str, Any]:
        return dict(base_path=self.base_path, base_area_dir=self.staging_container)

    @property
    def public_props(self) -> Dict[str, Any]:
        return dict(base_path=self.base_path, base_area_dir=self.public_container)


class AzureBlobFileSystemConfig(FileSystemConfig):
    @property
    def account_name(self) -> str:
        return self.file_system_cfg.get('account_name')

    @property
    def account_key(self) -> str:
        return self.file_system_cfg.get('account_key')

    @property
    def landing_props(self) -> Dict[str, Any]:
        return dict(storage_account_name=self.account_name,
                    storage_account_key=self.account_key,
                    area_container=self.landing_container)

    @property
    def staging_props(self) -> Dict[str, Any]:
        return dict(storage_account_name=self.account_name,
                    storage_account_key=self.account_key,
                    area_container=self.staging_container)

    @property
    def public_props(self) -> Dict[str, Any]:
        return dict(storage_account_name=self.account_name,
                    storage_account_key=self.account_key,
                    area_container=self.public_container)


class FileSystemType:
    blob = 'blob'
    local = 'local'


class WebConfig(NamedTuple):
    fs: str
    attrs: dict


def parse_web_config(web_cfg) -> WebConfig:
    log.debug(web_cfg)
    fs = web_cfg['fs']
    attrs_map = {
        FileSystemType.local: dict(base_path=web_cfg['base_path'],
                                   base_area_dir=web_cfg['container']),
        FileSystemType.blob: dict(storage_account_name=web_cfg['account_name'],
                                  storage_account_key=web_cfg['account_key'],
                                  area_container=web_cfg['container'])
    }

    if fs not in attrs_map:
        raise ValueError(f'Unsupported filesystem type `{fs}`. '
                         f'Available options: {",".join(attrs_map.keys())}')

    return WebConfig(fs=fs, attrs=attrs_map[fs])


class Config(BaseConfig):
    """Configuration is a Singleton and will be using just one configuration instance

    Priorities of how to get the configuration:
        1. Passed env during initialization of the class
        2. Environment variable `ENV`
        4. Using `local.yml` config if exists
        3. Using `default.yml` config
    """

    def __init__(self, env: str = None, dbutils=None):
        """Init configuration

        :param env: environment on which the database configuration should be obtained
        """
        log.info(f'ENV: {os.environ.get("ENV")}')
        self.env = env or os.environ.get('ENV') or ('local'
                                                    if BaseYmlConfigReader(env='local').exists()
                                                    else None) or 'default'
        self.__cfg = BaseYmlConfigReader(self.env, dbutils=dbutils).config
        log.info(f"Full config: {self.__cfg}")
        log.info(f'Configuration loaded for env: {self.env}')

        file_system_type_map: Mapping[str, type(FileSystemConfig)] = {
            FileSystemType.blob: AzureBlobFileSystemConfig,
            FileSystemType.local: LocalFileSystemConfig
        }
        if self.file_system_type not in file_system_type_map:
            raise ValueError(f'Unsupported file system type {self.file_system_type}')

        self.file_system: FileSystemConfig = file_system_type_map[self.file_system_type](self.__cfg)
        self.web_config: WebConfig = parse_web_config(self.__cfg['web'])

    def __getitem__(self, key):
        """Get item from configuration dict

        :param key: key
        :return: item
        """
        return self.__cfg.get(key)

    @property
    def file_system_type(self) -> str:
        return self.__cfg.get('file_system', dict()).get('type', '')

    @property
    def bq(self) -> dict:
        return self.__cfg.get('bq', dict())

    @property
    def bq_secret(self) -> dict:
        secret = self.bq.get('secret')
        if secret:
            return json.loads(secret)
        return dict()

    @property
    def bq_project(self) -> str:
        return self.bq.get('project', '')

    @property
    def github_token(self) -> str:
        return self.__cfg.get('github', dict()).get('token', '')

    @property
    def default_company(self) -> str:
        return self.__cfg.get('company', dict()).get('default', '')

    @property
    def spark_conf(self) -> Dict[str, str]:
        return self.__cfg.get('spark', dict())
