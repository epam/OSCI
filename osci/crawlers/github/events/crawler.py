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
from typing import Iterator, Iterable

from osci.crawlers.github.rest import GithubArchiveRest, GithubRest

from .unpack import decompress_json_lines
from .parser import (Event, PushEventCommit, parse_events, get_daily_events,
                     get_push_events, get_push_events_commits, get_company_commits_by_email_domain)

import logging

log = logging.getLogger(__name__)


def get_hour_events(day: datetime, rest: GithubArchiveRest) -> Iterator[Event]:
    hour_content = rest.get_hourly_events(date=day)
    if hour_content is not None:
        hour_json_payloads = decompress_json_lines(content=hour_content)
        return parse_events(payloads=hour_json_payloads)
    return []


def get_hour_push_events_commits(day: datetime, rest: GithubArchiveRest) -> Iterator[PushEventCommit]:
    events = get_hour_events(day=day, rest=rest)
    push_events = get_push_events(events=events)
    return get_push_events_commits(push_events=push_events)


def get_repository_events(repository_name: str, rest: GithubRest) -> Iterator[Event]:
    return parse_events(payloads=rest.get_repository_events(repo_name=repository_name))


def get_repositories_events(repositories_names: Iterable[str], rest: GithubRest) -> Iterator[Event]:
    for repo_name in repositories_names:
        yield from get_repository_events(repository_name=repo_name, rest=rest)


def get_company_repositories_events_commits(repositories_names: Iterable[str],
                                            company: str,
                                            date: datetime,
                                            rest: GithubRest) -> Iterator[PushEventCommit]:
    events = get_repositories_events(repositories_names=repositories_names, rest=rest)
    daily_events = get_daily_events(events=events, date=date)
    push_events = get_push_events(events=daily_events)
    push_events_commits = get_push_events_commits(push_events=push_events)
    return get_company_commits_by_email_domain(commits=push_events_commits, company=company)
