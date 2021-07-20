"""Copyright since 2020, EPAM Systems

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

from typing import NamedTuple


class RepositoriesSchema(NamedTuple):
    name = 'name'

    language = 'language'
    license = 'license'

    downloaded_at = 'downloaded_at'

    required = [name, language, license, downloaded_at]


class PushEventsCommitsSchema(NamedTuple):
    event_id = 'event_id'
    event_created_at = 'event_created_at'

    repo_name = 'repo_name'
    org_name = 'org_name'
    actor_login = 'actor_login'

    sha = 'sha'
    author_name = 'author_name'
    author_email = 'author_email'

    company = 'company'

    language = RepositoriesSchema().language
    license = RepositoriesSchema().license

    required = [event_id, event_created_at, repo_name,
                org_name, actor_login, sha, author_name,
                author_email, company, language, license]


class StagingSchemas:
    push_commits: PushEventsCommitsSchema = PushEventsCommitsSchema()
    repositories: RepositoriesSchema = RepositoriesSchema()
