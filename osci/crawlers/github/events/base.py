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

from osci.utils import parse_date_field
from typing import NamedTuple


class Repository(NamedTuple):
    id: int = None
    name: str = None
    url: str = None


class Actor(NamedTuple):
    id: int = None
    login: str = None
    display_login: str = None
    url: str = None


class Organization(NamedTuple):
    id: int = None
    login: str = None
    url: str = None


class Event:

    def __init__(self, json_payload: dict = None):
        json_payload = json_payload or dict()

        self.public = json_payload.get('public')

        self.payload = json_payload.get('payload')

        rw = json_payload.get('repo', dict())
        self.repository = Repository(id=rw.get('id'), name=rw.get('name'), url=rw.get('url'))

        rw = json_payload.get('actor', dict())
        self.actor = Actor(id=rw.get('id'), login=rw.get('login'),
                           display_login=rw.get('display_login'), url=rw.get('url'))

        rw = json_payload.get('org', dict())
        self.organization = Organization(id=rw.get('id'), login=rw.get('login'), url=rw.get('url'))

        self.created_at = parse_date_field(json_payload.get('created_at'))

        self.id = json_payload.get('id')
