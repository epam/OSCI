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
import datetime
import pandas as pd

from osci.datalake import DataLake
from osci.datalake.reports.company.new_contributors import NewContributors
from osci.datalake.reports.company.new_repos import NewRepos
from osci.datalake.reports.company.contributors_repos import ContributorsReposYTD
from osci.postprocess.osci_change_report import get_previous_date


def get_contributors_repositories_change(date: datetime, company: str):
    ranking = ContributorsReposYTD(date=date, company=company)
    ranking_df = ranking.read()
    compared_ranking = ContributorsReposYTD(date=get_previous_date(date), company=company)
    compared_ranking_df = compared_ranking.read()

    new_contributors = NewContributors(date=date, company=company)

    new_contributors_df = pd.DataFrame(
        data=set(ranking_df[ranking.schema.author]) - set(compared_ranking_df[ranking.schema.author]),
        columns=[DataLake().public.schemas.new_contributors.author]
    )
    new_contributors.save(df=new_contributors_df)

    new_repos = NewRepos(date=date, company=company)

    new_repos_df = pd.DataFrame(
        data=set(ranking_df[ranking.schema.repo]) - set(compared_ranking_df[ranking.schema.repo]),
        columns=[DataLake().public.schemas.new_repos.repo]
    )
    new_repos.save(df=new_repos_df)
