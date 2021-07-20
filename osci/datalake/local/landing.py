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

from .base import LocalSystemArea
from osci.datalake.base import BaseLandingArea
from osci.utils import get_pandas_data_frame_info

from datetime import datetime
from pathlib import Path

import logging
import pandas as pd

log = logging.getLogger(__name__)


class LocalLandingArea(BaseLandingArea, LocalSystemArea):
    BASE_AREA_DIR = 'landing'

    @staticmethod
    def get_push_events_commits_filename(date: datetime, file_format='parquet'):
        return date.strftime(f"%Y-%m-%d-{date.hour}.{file_format}")

    def save_push_events_commits(self, push_event_commits, date: datetime):
        file_path = self._get_hourly_push_events_commits_path(date)
        df = pd.DataFrame(push_event_commits)
        log.info(f'Save push events commits for {date} into file {file_path}')
        log.info(f'Push events commits df info {get_pandas_data_frame_info(df)}')
        df.to_parquet(str(file_path), engine='pyarrow', index=False)

    def get_hour_push_events_commits(self, date: datetime):
        file_path = self._get_hourly_push_events_commits_path(date)
        log.info(f'Read push events commits for {date.strftime("%Y-%m-%d %H:00")} from file {file_path}')
        if file_path.is_file():
            df = pd.read_parquet(path=file_path, engine='pyarrow')
            log.info(f'Push events commits {date.strftime("%Y-%m-%d %H:00")} df info {get_pandas_data_frame_info(df)}')
            return df
        else:
            log.warning(f'Not such push events commits file for {date} in path {file_path}')
            return None

    def get_daily_push_events_commits(self, date: datetime):
        log.info(f'Read push events commits for {date.strftime("%Y-%m-%d")}')
        df = pd.DataFrame()
        for hour in range(24):
            date = date.replace(hour=hour)
            hour_df = self.get_hour_push_events_commits(date=date)
            if hour_df is not None:
                df = pd.concat([df, hour_df])
        return df

    def get_push_events_commits_parent_dir(self, date: datetime, create_if_not_exists=False):
        path = self._github_events_commits_base / date.strftime("%Y") / date.strftime("%m") / date.strftime("%d")
        if create_if_not_exists:
            path.mkdir(parents=True, exist_ok=True)
        return path

    def _get_hourly_push_events_commits_path(self, date: datetime) -> Path:
        return self.get_push_events_commits_parent_dir(date=date, create_if_not_exists=True) / \
               self.get_push_events_commits_filename(date)

    def _get_repository_file_path(self, date: datetime) -> Path:
        path = self.BASE_PATH / self.BASE_AREA_DIR / self._github_repositories_base / date.strftime("%Y") / date.strftime("%m")
        path.mkdir(parents=True, exist_ok=True)
        return path / f'{date:%Y-%m-%d}.csv'

    def save_repositories(self, df: pd.DataFrame, date: datetime):
        df.to_csv(self._get_repository_file_path(date=date), index=False)

    def get_repositories(self, date: datetime) -> pd.DataFrame:
        file_path = self._get_repository_file_path(date=date)
        log.debug(f'Read repositories names for {date:%Y-%m-%d} from file {file_path}')
        if file_path.is_file():
            df = pd.read_csv(file_path)
            log.debug(f'Repositories names {date:%Y-%m-%d} df info {get_pandas_data_frame_info(df)}')
            return df
        else:
            log.warning(f'Not such repositories names file for {date:%Y-%m-%d} in path {file_path}')
            return pd.DataFrame()
