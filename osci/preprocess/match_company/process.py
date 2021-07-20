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
import datetime
import logging

from .push_commits import process_push_commits

from osci.datalake import DataLake

log = logging.getLogger(__name__)


def process_github_daily_push_events(day: datetime.datetime):
    push_events_commits = DataLake().landing.get_daily_push_events_commits(date=day)
    if push_events_commits is not None and not push_events_commits.empty:
        companies_events = process_push_commits(push_events_commits,
                                                email_field=DataLake().landing.schemas.push_commits.author_email,
                                                company_field=DataLake().staging.schemas.push_commits.company,
                                                datetime_field=DataLake().landing.schemas.push_commits.event_created_at)
        for company, commits in companies_events:
            log.debug(f'Save company {company}')
            DataLake().staging.save_raw_push_events_commits(push_event_commits=commits, date=day, company_name=company)
