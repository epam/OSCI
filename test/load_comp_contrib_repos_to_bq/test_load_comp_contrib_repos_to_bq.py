import pandas as pd
import pytest
from datetime import datetime
from osci.datalake.reports.general import CompaniesContributorsRepository
from osci.publishing import load_companies_contrib_repos_to_bq


@pytest.fixture()
def load_date():
    return datetime(year=2021, month=1, day=1)


@pytest.fixture()
def comp_contrib_repos_df():
    return pd.DataFrame([
        {CompaniesContributorsRepository.schema.author_name: "Author Name",
         CompaniesContributorsRepository.schema.author_email: "email@email.com",
         CompaniesContributorsRepository.schema.company: "Company",
         CompaniesContributorsRepository.schema.commits: 11111,
         CompaniesContributorsRepository.schema.license: "other",
         CompaniesContributorsRepository.schema.repository: "repo/name",
         CompaniesContributorsRepository.schema.language: "python",
         CompaniesContributorsRepository.schema.date: datetime(year=2021, month=1, day=1)
         }])


@pytest.mark.skip(reason="each calling function has a cost")
def test_load_repos_contrib_repos_to_bq(mocker, comp_contrib_repos_df, load_date):
    mocker.patch("osci.datalake.CompaniesContributorsRepository.read", return_value=comp_contrib_repos_df)
    res = load_companies_contrib_repos_to_bq(load_date)
    assert res is not None
