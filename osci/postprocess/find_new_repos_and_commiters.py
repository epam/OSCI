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
