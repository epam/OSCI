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
from datetime import datetime

from osci.crawlers.github.events.crawler import get_company_repositories_events_commits
from osci.crawlers.github.rest import GithubRest
from osci.config import Config
from osci.datalake import DataLake, DatePeriodType

import pandas as pd
import logging

log = logging.getLogger(__name__)


def load_company_repositories_events_commits(date: datetime, company: str):
    events = DataLake().staging.get_push_events_commits(company=company,
                                                        from_date=date,
                                                        to_date=date,
                                                        date_period_type=DatePeriodType.DTD)
    schema = DataLake().staging.schemas.push_commits
    if events.empty:
        log.warning(f'No {company} events at {date}')
        return
    with GithubRest(token=Config().github_token) as rest:
        company_commits = get_company_repositories_events_commits(repositories_names=events[schema.repo_name].unique(),
                                                                  date=date,
                                                                  company=company,
                                                                  rest=rest)
        company_commits_df = pd.DataFrame(company_commits)
        DataLake().staging.save_private_push_events_commits(push_event_commits=company_commits_df,
                                                            company_name=company,
                                                            date=date)
