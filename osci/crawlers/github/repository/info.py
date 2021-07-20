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
from typing import NamedTuple, Optional, Dict, Any
from datetime import datetime, date


class Repository(NamedTuple):
    name: str
    short_name: Optional[str]

    language: Optional[str]
    license: Optional[str]

    is_fork: Optional[bool]

    stargazers_count: int
    watchers_count: int
    forks_count: int
    network_count: int
    subscribers_count: int

    created_at: datetime
    updated_at: datetime
    pushed_at: datetime

    downloaded_at: date


def _parse_optional_datetime(dt: Optional[str]) -> Optional[datetime]:
    if dt is not None and isinstance(dt, str):
        return datetime.fromisoformat(dt.replace('Z', ''))


def parse_get_repository_response(resp: Dict[str, Any], downloaded_at: date) -> Repository:
    return Repository(name=resp['full_name'],
                      short_name=resp.get('name', ''),

                      language=resp.get('language'),
                      license=resp.get('license').get('key') if isinstance(resp.get('license'), dict) else None,

                      is_fork=resp.get('fork'),

                      stargazers_count=resp.get('stargazers_count'),
                      watchers_count=resp.get('watchers_count'),
                      forks_count=resp.get('forks_count'),
                      network_count=resp.get('network_count'),
                      subscribers_count=resp.get('subscribers_count'),

                      created_at=_parse_optional_datetime(resp.get('created_at')),
                      updated_at=_parse_optional_datetime(resp.get('updated_at')),
                      pushed_at=_parse_optional_datetime(resp.get('pushed_at')),

                      downloaded_at=downloaded_at)
