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
from osci.datalake.base import BaseLandingArea
from osci.utils import get_pandas_data_frame_info

from datetime import datetime

import logging
import pandas as pd

log = logging.getLogger(__name__)


class BlobLandingArea(BaseLandingArea, BlobArea):
    AREA_CONTAINER = 'landing'

    def save_push_events_commits(self, push_event_commits, date: datetime, index=False):
        file_path = self._get_hourly_push_events_commits_path(date)

        df = pd.DataFrame(push_event_commits)

        log.info(f'Save push events commits for {date} into file {file_path}')
        log.info(f'Push events commits df info {get_pandas_data_frame_info(df)}')

        self.write_pandas_dataframe_to_parquet(df, file_path, index=index)

    def get_hour_push_events_commits(self, date: datetime):
        file_path = self._get_hourly_push_events_commits_path(date)

        log.info(f'Read push events commits for {date.strftime("%Y-%m-%d %H:00")} from file {file_path}')
        df = self.read_pandas_dataframe_from_parquet(path=file_path)
        if df is not None:
            log.debug(f'Push events commits {date.strftime("%Y-%m-%d %H:00")} df info {get_pandas_data_frame_info(df)}')
            return df

    def get_daily_push_events_commits(self, date: datetime):

        log.info(f'Read push events commits for {date.strftime("%Y-%m-%d")}')
        df = pd.DataFrame()
        for hour in range(24):
            date = date.replace(hour=hour)
            hour_df = self.get_hour_push_events_commits(date=date)
            if hour_df is not None:
                df = pd.concat([df, hour_df])
        return df

    def _get_hourly_push_events_commits_path(self, date: datetime) -> str:
        return date.strftime(f"{self._github_events_commits_base}/%Y/%m/%d/%Y-%m-%d-{date.hour}.parquet")

    def _get_repository_file_path(self, date: datetime) -> str:
        return f'{self._github_repositories_base}/{date:%Y/%m/%Y-%m-%d}.csv'

    def save_repositories(self, df: pd.DataFrame, date: datetime):
        self.write_pandas_dataframe_to_csv(df=df, path=self._get_repository_file_path(date=date))

    def get_repositories(self, date: datetime) -> pd.DataFrame:
        return self.read_pandas_dataframe_from_csv(path=self._get_repository_file_path(date=date))
