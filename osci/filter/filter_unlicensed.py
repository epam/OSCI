"""Copyright since 2021, EPAM Systems

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
from datetime import datetime
from typing import List
from osci.datalake import DataLake
from osci.datalake.repositories import Repositories

import logging
import pandas as pd

log = logging.getLogger(__name__)


def filter_and_adjunct_push_event_commit(df: pd.DataFrame, licensed_repos_df: pd.DataFrame, filter_columns: List[str],
                                         adjunct_columns: List[str], default_columns: List[str], right_index: str = "",
                                         left_index: str = "") -> pd.DataFrame:
    """Adjunct dataframe and filter DataFrame without license

    :param df: push event commit dataframe
    :param licensed_repos_df: licensed repository dataframe
    :param filter_columns: filter columns
    :param adjunct_columns: Columns, that are added tp `df`
    :param default_columns:  Default required columns in schema
    :param left_index: column name on df
    :param right_index: column index on licensed_repos_df
    """
    try:
        return df.join(licensed_repos_df[adjunct_columns].set_index(right_index),
                       on=left_index).dropna(subset=filter_columns).reset_index(drop=True)

    except KeyError as ex:
        log.warning("`licensed_repos_df` or `df` is empty \n"
                    f"{licensed_repos_df.info()} , {df.info()}")
        log.exception(ex)
        return pd.DataFrame(columns=default_columns)


def filter_out_unlicensed(date: datetime):
    """Read row PEC, filter and save them with license, language

    :param date: push events on this day
    """
    log.debug(f'Filter out unlicensed push events commits for date {date:%Y-%m-%d}')
    log.debug(f'Read licensed repos for date {date:%Y-%m-%d}')
    licensed_repos_df = Repositories(date=date).read()

    for company, df in DataLake().staging.get_daily_raw_push_events_commits(date):
        log.debug(f'Filter out unlicensed push events commits for date {date:%Y-%m-%d} for {company}')
        filtered_df = filter_and_adjunct_push_event_commit(df, licensed_repos_df,
                                                           [DataLake().staging.schemas.repositories.license],
                                                           [DataLake().staging.schemas.repositories.name,
                                                            DataLake().staging.schemas.repositories.language,
                                                            DataLake().staging.schemas.repositories.license
                                                            ],
                                                           DataLake().staging.schemas.push_commits.required,
                                                           right_index=DataLake().staging.schemas.repositories.name,
                                                           left_index=DataLake().staging.schemas.push_commits.repo_name
                                                           )
        if not filtered_df.empty:
            DataLake().staging.save_push_events_commits(
                push_event_commits=filtered_df,
                company_name=company,
                date=date
            )
