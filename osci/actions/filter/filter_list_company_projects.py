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
from osci.datalake import DataLake
from osci.datalake.reports.company.repos import ReposRankingMTD
from osci.filter.filter_list_company_projects import filter_projects

from datetime import datetime


class FilterListCompanyProjectsAction(Action):
    """Filter list company projects"""

    params = Action.params + (
        ActionParam(name='company', short_name='c', type=str, required=True),
    )

    @classmethod
    def name(cls):
        return 'filter-list-company-projects'

    @classmethod
    def help_text(cls) -> str:
        return "Filter list company projects and save as a report"

    def _execute(self, day: datetime, company: str):
        df = ReposRankingMTD(date=day, company=company).read()
        out_df = filter_projects(df=df,
                                 projects_filter_list=DataLake().staging.load_projects_filter(),
                                 commits_amount_field=DataLake().public.schemas.repo_commits_ranking.commits,
                                 repo_name_field=DataLake().public.schemas.repo_commits_ranking.repo)
        DataLake().public.save_report(report_df=out_df,
                                      report_name='projects_activity_MTD',
                                      date=day, company=company)
