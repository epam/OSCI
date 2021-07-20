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
from google.cloud import bigquery
from google.oauth2 import service_account

import logging
import pandas as pd

log = logging.getLogger(__name__)


class BigQuery:

    def __init__(self, project: str, client_secrets: dict):
        self.project = project
        self.client_secrets = client_secrets
        self.__client = None

    def __setup_client(self) -> bigquery.Client:
        credentials = service_account.Credentials.from_service_account_info(
            self.client_secrets,
            scopes=['https://www.googleapis.com/auth/bigquery']
        )
        self.__client = bigquery.Client(project=self.project, credentials=credentials)
        return self.__client

    @property
    def client(self) -> bigquery.Client:
        return self.__client if self.__client is not None else self.__setup_client()

    def load_dataframe(self, df: pd.DataFrame, table_id: str, schema: list = None):
        job_config = bigquery.LoadJobConfig(schema=schema if schema is not None else [])
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        return self.client.get_table(table_id)
