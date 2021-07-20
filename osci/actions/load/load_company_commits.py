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
from osci.load.company_commits import load_company_repositories_events_commits
from osci.actions import Action, ActionParam
from datetime import datetime


class LoadCompanyCommitsAction(Action):
    """Load company commits for the day"""

    params = Action.params + (
        ActionParam(name='company', short_name='c', type=str, required=True, description='Company name'),
    )

    @classmethod
    def name(cls) -> str:
        return 'load-company-commits'

    @classmethod
    def help_text(cls) -> str:
        return "Load company repositories events commits"

    def _execute(self, day: datetime, company: str):
        return load_company_repositories_events_commits(date=day, company=company)
