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
from osci.actions import Action
from datetime import datetime
from osci.postprocess.get_num_repos_per_company import get_num_repos_per_company
from osci.datalake.reports.general.repos_per_company import RepositoriesPerCompanyDTD


class GetNumberOfRepositoriesPerCompanyAction(Action):
    """Count number of repositories per company"""

    @classmethod
    def name(cls) -> str:
        return 'get-number-of-repositories-per-company'

    def _execute(self, day: datetime):
        report = RepositoriesPerCompanyDTD(date=day)
        report.save(get_num_repos_per_company(date=day))
        return report
