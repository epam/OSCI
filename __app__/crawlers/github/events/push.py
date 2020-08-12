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

from typing import Iterator, NamedTuple
from datetime import datetime

from .base import Event

import logging

log = logging.getLogger(__name__)


class PushEventCommit(NamedTuple):
    event_id: int
    event_created_at: datetime

    repo_name: str
    org_name: str
    actor_login: str

    sha: str
    author_name: str
    author_email: str


class PushEvent(Event):

    def get_pure_commits(self) -> Iterator[dict]:
        commits = self.payload.get('commits')
        if commits:
            for commit in commits:
                author = commit.get('author')
                lined_commit = commit.copy()
                if author:
                    lined_commit['author_name'] = author.get('name')
                    lined_commit['author_email'] = author.get('email')
                yield lined_commit

    def get_commits(self) -> Iterator[PushEventCommit]:
        for commit in self.get_pure_commits():
            yield PushEventCommit(event_id=self.id,
                                  event_created_at=self.created_at,
                                  repo_name=self.repository.name,
                                  org_name=self.organization.login,
                                  actor_login=self.actor.login,
                                  sha=commit.get('sha'),
                                  author_name=commit.get('author_name'),
                                  author_email=commit.get('author_email'))
