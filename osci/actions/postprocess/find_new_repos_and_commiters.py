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
from osci.actions import Action, ActionParam
from osci.postprocess.find_new_repos_and_commiters import get_contributors_repositories_change
from datetime import datetime


class FindContributorsRepositoriesChangeAction(Action):
    """Load company commits for the day"""

    params = Action.params + (
        ActionParam(name='company', type=str, required=True, short_name='c', description='Company name'),
    )

    @classmethod
    def name(cls) -> str:
        return 'find-contributors-repositories-change'

    def _execute(self, day: datetime, company: str):
        return get_contributors_repositories_change(date=day, company=company)
