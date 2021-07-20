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
import datetime
import logging
import pandas as pd

from osci.datalake import DataLake, DatePeriodType
from osci.datalake.schemas import LandingSchemas
from osci.blacklist import Blacklist

log = logging.getLogger(__name__)


def get_daily_active_repositories(date: datetime.datetime) -> pd.DataFrame:
    df = DataLake().staging.get_union_daily_raw_push_events_commits(date=date)
    result_df = df[[LandingSchemas.push_commits.repo_name]].drop_duplicates()
    result_df = result_df[
        result_df.apply(lambda row: not Blacklist().is_blocked_repo_by_account(
            repository_name=row[LandingSchemas.push_commits.repo_name]
        ), axis=1)
    ]
    DataLake().landing.save_repositories(df=result_df, date=date)
    return result_df
