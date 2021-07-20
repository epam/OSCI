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
import yaml

from osci.utils import get_pandas_data_frame_info, get_azure_blob_connection_string
from osci.datalake.base import BaseDataLakeArea

from azure.storage.blob import BlobServiceClient, ContainerClient, ContentSettings
from azure.core.exceptions import ResourceNotFoundError
from io import BytesIO, StringIO

import logging
import pandas as pd
import pyarrow.parquet as pq

log = logging.getLogger(__name__)


class BlobArea(BaseDataLakeArea):
    AREA_CONTAINER = None

    @property
    def _github_events_commits_base(self):
        return 'github/events/push'

    @property
    def _github_repositories_base(self):
        return 'github/repository'

    _github_raw_events_commits_base = 'github/raw-events/push'

    def __init__(self, storage_account_name: str, storage_account_key: str, *args,
                 area_container: str = AREA_CONTAINER, **kwargs):
        super().__init__(*args, **kwargs)
        self.AREA_CONTAINER = area_container
        self.storage_account_name = storage_account_name
        self.storage_account_key = storage_account_key
        connection_string = get_azure_blob_connection_string(account_name=self.storage_account_name,
                                                             account_key=self.storage_account_key)
        self.blob_service: BlobServiceClient = BlobServiceClient.from_connection_string(conn_str=connection_string)
        self.container_client: ContainerClient = self.blob_service.get_container_client(container=self.AREA_CONTAINER)
        log.debug(f'BLOB Data Lake area {self.AREA_CONTAINER} created')

    def add_fs_prefix(self, path: str) -> str:
        return f'wasbs://{self.AREA_CONTAINER}@{self.storage_account_name}.blob.core.windows.net/{path}'

    def add_http_prefix(self, path: str) -> str:
        return f'https://{self.storage_account_name}.blob.core.windows.net/{self.AREA_CONTAINER}/{path}'

    def write_pandas_dataframe_to_parquet(self, df: pd.DataFrame, path: str, index=False):
        """Writes pandas dataframe to parquet to blob

        :param df: dataframe to write
        :param path: blob name to save
        :param index: write index column
        """
        with BytesIO() as buffer:
            log.debug(f"Save pandas df to {self.AREA_CONTAINER}/{path}; df.info: {get_pandas_data_frame_info(df)}")
            df.to_parquet(buffer, engine='pyarrow', index=index)
            container_client = self.blob_service.get_container_client(container=self.AREA_CONTAINER)
            container_client.upload_blob(name=path, data=buffer.getvalue(), overwrite=True)

    def read_pandas_dataframe_from_parquet(self, path: str) -> pd.DataFrame:
        """Load parquet data from azure blob to pandas dataframe

        :param path: blob_name to load
        :return: pandas dataframe from blob
        """
        blob_client = self.blob_service.get_blob_client(container=self.AREA_CONTAINER, blob=path)
        try:
            with BytesIO(blob_client.download_blob().readall()) as buffer:
                return pq.read_table(source=buffer).to_pandas()
        except ResourceNotFoundError as ex:
            log.error(f"ResourceNotFound {ex}")

    def write_pandas_dataframe_to_csv(self, df: pd.DataFrame, path: str, index=False):
        """Writes pandas dataframe to csv to blob

        :param df: dataframe to write
        :param path: blob name to save
        :param index: write index column
        """
        with StringIO() as buffer:
            log.debug(f"Save pandas df to {self.AREA_CONTAINER}/{path}; df.info: {get_pandas_data_frame_info(df)}")
            df.to_csv(buffer, index=index)
            container_client = self.blob_service.get_container_client(container=self.AREA_CONTAINER)
            container_client.upload_blob(name=path, data=buffer.getvalue(), overwrite=True)

    def read_pandas_dataframe_from_csv(self, path: str, dtype=None) -> pd.DataFrame:
        """Load parquet data from azure blob to pandas dataframe

        :param path: blob_name to load
        :param dtype: Type name or dict of column -> type, optional
        :return: pandas dataframe from blob
        """
        blob_client = self.blob_service.get_blob_client(container=self.AREA_CONTAINER, blob=path)
        try:
            with StringIO(blob_client.download_blob().readall().decode()) as buffer:
                return pd.read_csv(buffer, dtype=dtype)
        except ResourceNotFoundError as ex:
            log.error(f"ResourceNotFound {ex}")

    def write_bytes_to_file(self, path: str, buffer: BytesIO):
        container_client = self.blob_service.get_container_client(container=self.AREA_CONTAINER)
        container_client.upload_blob(name=path, data=buffer.getvalue(), overwrite=True)

    def write_string_to_file(self, path: str, data: str, content_type: str = 'application/octet-stream'):
        with StringIO(data) as buffer:
            container_client = self.blob_service.get_container_client(container=self.AREA_CONTAINER)
            container_client.upload_blob(name=path, data=buffer.getvalue(), overwrite=True,
                                         content_settings=ContentSettings(content_type=content_type))

    def read_yaml_file(self, path: str):
        log.info(f'Read yml from path: {path}')
        blob_client = self.blob_service.get_blob_client(container=self.AREA_CONTAINER, blob=path)
        try:
            with StringIO(blob_client.download_blob().readall().decode()) as buffer:
                return yaml.load(buffer, Loader=yaml.FullLoader)
        except ResourceNotFoundError as ex:
            log.error(f"ResourceNotFound {ex}")
