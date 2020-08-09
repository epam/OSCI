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

from .base import BlobArea
from __app__.datalake.base import BaseStagingArea, DatePeriodType
from __app__.utils import get_pandas_data_frame_info, normalize_company

from datetime import datetime
from typing import Union, Iterable, List

import logging
import pandas as pd

log = logging.getLogger(__name__)


class BlobStagingArea(BaseStagingArea, BlobArea):
    AREA_CONTAINER = 'staging'

    def get_push_events_commits(self, push_event_commits_path):
        return self.read_pandas_dataframe_from_parquet(path=push_event_commits_path)

    def get_push_events_commits_file_path(self, date: datetime, company: str):
        return f'{self.get_push_events_commits_parent_dir(date)}/{self.get_push_events_commits_filename(date, company)}'

    @staticmethod
    def _get_file_name(path: str) -> str:
        return path.split('/').pop()

    def save_push_events_commits(self, push_event_commits: pd.DataFrame, company_name: str, date: datetime):
        file_path = self.get_push_events_commits_file_path(date=date, company=company_name)

        log.info(f'Save push events commits for {date} into file {file_path}\n'
                 f'DF INFO: {get_pandas_data_frame_info(push_event_commits)}')
        self.write_pandas_dataframe_to_parquet(push_event_commits, file_path, index=False)

    def get_push_events_commits_spark_paths(self, to_date: datetime, date_period_type: str = DatePeriodType.YTD,
                                            from_date: datetime = None, company=None) -> List[str]:
        return self.get_spark_paths(self.get_push_events_commits_paths(to_date=to_date,
                                                                       date_period_type=date_period_type,
                                                                       from_date=from_date,
                                                                       company=company))

    push_commits_filename_pattern = r'^(?P<company>(\d|\w|_)+)-(?P<date>\d{4}-\d{2}-\d{2}).parquet$'

    def get_push_events_commits_parent_dir(self, date: datetime) -> str:
        return date.strftime(f'{self._github_events_commits_base}/%Y/%m/%d')

    @staticmethod
    def get_push_events_commits_filename(date: datetime, company: str) -> str:
        return date.strftime(f'{normalize_company(name=company)}-%Y-%m-%d.parquet')

    def _get_date_partitioned_paths(self, dir_path: str, year: Union[str, int] = None,
                                    month: Union[str, int] = None,
                                    day: Union[str, int] = None,
                                    company: str = None) -> Iterable[str]:
        dir_path += '/'
        if year is not None:
            dir_path += f'{year}/'
            if month is not None:
                dir_path += f'{str(month).zfill(2)}/'
                if day is not None:
                    dir_path += f'{str(day).zfill(2)}/'
                    if company is not None:
                        dir_path += f'{normalize_company(name=company)}-'

        return (blob['name'] for blob in self.container_client.list_blobs(prefix=dir_path))
