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
from typing import Iterator

from __app__.crawlers.github.rest import GithubArchiveRest

from .unpack import decompress_json_lines
from .parser import parse_events, Event, get_push_events, get_push_events_commits, PushEventCommit


def get_hour_events(day: datetime, rest: GithubArchiveRest) -> Iterator[Event]:
    hour_content = rest.get_hourly_events(date=day)
    hour_json_payloads = decompress_json_lines(content=hour_content)
    return parse_events(payloads=hour_json_payloads)


def get_hour_push_events_commits(day: datetime, rest: GithubArchiveRest) -> Iterator[PushEventCommit]:
    events = get_hour_events(day=day, rest=rest)
    push_events = get_push_events(events=events)
    return get_push_events_commits(push_events=push_events)
