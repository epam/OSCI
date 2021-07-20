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
from osci.datalake.repositories import Repositories
from osci.datalake import DataLake
from osci.crawlers.github.rest import GithubRest
from osci.crawlers.github.repository.info import parse_get_repository_response
from osci.config import Config

from datetime import datetime
from typing import Iterable

import pandas as pd
import logging

log = logging.getLogger(__name__)


def _load_repositories(repos_names: Iterable[str]) -> pd.DataFrame:
    def _repositories(names: Iterable[str]):
        with GithubRest(token=Config().github_token) as rest:
            for name in names:
                try:
                    repo_resp = rest.get_repository(repo_name=name)
                    if repo_resp is not None:
                        repository = parse_get_repository_response(repo_resp, downloaded_at=datetime.now().date())
                        if repository.__getattribute__(Repositories.schema.license):
                            yield {field: repository.__getattribute__(field)
                                   for field in Repositories.schema.required}
                except Exception as ex:
                    log.error(f'Failed loading repository {name}. ex: {ex}')

    return pd.DataFrame(_repositories(names=repos_names), columns=Repositories.schema.required)


def load_repositories(date: datetime) -> pd.DataFrame:
    log.debug(f'Load repositories information for {date:%Y-%m-%d}')
    repositories = Repositories(date=date)
    df = pd.DataFrame(data=[], columns=Repositories.schema.required)
    repositories_names = DataLake().landing.get_repositories(date=date)

    if not repositories_names.empty:
        df = _load_repositories(repos_names=repositories_names[DataLake().landing.schemas.repositories_names.name])

    repositories.save(df)
    return df
