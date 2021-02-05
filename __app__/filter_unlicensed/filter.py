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
from __app__.datalake import DataLake
from __app__.datalake.repositories import Repositories

import logging

log = logging.getLogger(__name__)


def filter_out_unlicensed(date: datetime):
    log.debug(f'Filter out unlicensed push events commits for date {date:%Y-%m-%d}')
    licensed_repos = Repositories(date=date)
    log.debug(f'Read licensed repos for date {date:%Y-%m-%d}')
    licensed_repos_df = licensed_repos.read()

    licensed_repos_set = frozenset(licensed_repos_df[licensed_repos.schema.name].tolist())

    for company, df in DataLake().staging.get_daily_raw_push_events_commits(date):
        log.debug(f'Filter out unlicensed push events commits for date {date:%Y-%m-%d} for {company}')
        filtered_df = df[df[DataLake().staging.schemas.push_commits.repo_name].isin(licensed_repos_set)]
        DataLake().staging.save_push_events_commits(push_event_commits=filtered_df, company_name=company, date=date)
