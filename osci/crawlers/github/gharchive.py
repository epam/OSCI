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

from .events.crawler import get_hour_push_events_commits
from .rest import GithubArchiveRest

from osci.datalake import DataLake

log = logging.getLogger(__name__)


def get_github_daily_push_events(day: datetime.datetime):
    with GithubArchiveRest() as rest:
        for hour in range(24):
            log.info(f'Crawl events for {day}')
            day = day.replace(hour=hour)
            push_events_commits = get_hour_push_events_commits(day=day, rest=rest)
            DataLake().landing.save_push_events_commits(push_event_commits=push_events_commits, date=day)
