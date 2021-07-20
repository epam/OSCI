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
from osci.postprocess.get_num_companies_commit_per_repo import get_num_companies_commit_per_repository
from osci.datalake.reports.general.companies_commits_per_repo import CompaniesCommitsPerRepositoriesDTD


class GetNumberOfCompaniesCommitsPerRepositoryAction(Action):
    """Count number companies commits per repositories"""

    @classmethod
    def name(cls) -> str:
        return 'get-number-of-companies-commits-per-repository'

    def _execute(self, day: datetime):
        report = CompaniesCommitsPerRepositoriesDTD(date=day)
        report.save(get_num_companies_commit_per_repository(date=day))
        return report
