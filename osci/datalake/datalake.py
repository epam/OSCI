"""Copyright since 2020, EPAM Systems

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
from typing import Tuple, Mapping, Callable, Type

from osci.utils import MetaSingleton
from osci.config import Config, FileSystemType

from .base import BaseLandingArea, BaseStagingArea, BasePublicArea, BaseWebArea
from .local import LocalLandingArea, LocalStagingArea, LocalPublicArea, LocalWebArea
from .blob import BlobLandingArea, BlobStagingArea, BlobPublicArea, BlobWebArea

from .bq import BigQuery


class DataLake(metaclass=MetaSingleton):
    landing: BaseLandingArea
    staging: BaseStagingArea
    public: BasePublicArea
    web: BaseWebArea
    big_query: BigQuery

    def __init__(self):
        fs_to_data_lake: Mapping[str, Callable[[], Tuple[BaseLandingArea, BlobStagingArea, BlobPublicArea]]] = {
            FileSystemType.blob: self.__get_blob_data_lakes,
            FileSystemType.local: self.__get_local_data_lakes,
        }

        fs_to_web_area: Mapping[str, Type[BaseWebArea]] = {
            FileSystemType.blob: BlobWebArea,
            FileSystemType.local: LocalWebArea,
        }
        self.landing, self.staging, self.public = fs_to_data_lake[Config().file_system_type]()
        self.web = fs_to_web_area[Config().web_config.fs](**Config().web_config.attrs)
        self.big_query = BigQuery(project=Config().bq_project, client_secrets=Config().bq_secret)

    @staticmethod
    def __get_local_data_lakes() -> Tuple[LocalLandingArea, LocalStagingArea, LocalPublicArea]:
        return (LocalLandingArea(**Config().file_system.landing_props),
                LocalStagingArea(**Config().file_system.staging_props),
                LocalPublicArea(**Config().file_system.public_props))

    @staticmethod
    def __get_blob_data_lakes() -> Tuple[BlobLandingArea, BlobStagingArea, BlobPublicArea]:
        return (BlobLandingArea(**Config().file_system.landing_props),
                BlobStagingArea(**Config().file_system.staging_props),
                BlobPublicArea(**Config().file_system.public_props))
