import pandas as pd
import pytest
from datetime import datetime
from osci.postprocess.get_num_companies_commit_per_repo import get_num_companies_commit_per_repository
from osci.datalake.schemas.public import NumberOfCompaniesCommitsInRepositories
from pandas._testing import assert_frame_equal
from osci.datalake import CompaniesContributorsRepository


@pytest.fixture()
def comp_contrib_repos_complex_df():
    return pd.DataFrame([
        {CompaniesContributorsRepository.schema.author_name: "Author Name",
         CompaniesContributorsRepository.schema.author_email: "email@email.com",
         CompaniesContributorsRepository.schema.company: "Company1",
         CompaniesContributorsRepository.schema.commits: 42,
         CompaniesContributorsRepository.schema.license: "other",
         CompaniesContributorsRepository.schema.repository: "repo/name",
         CompaniesContributorsRepository.schema.language: "python",
         CompaniesContributorsRepository.schema.date: datetime(year=2021, month=1, day=1)
         },
        {CompaniesContributorsRepository.schema.author_name: "Author Name2",
         CompaniesContributorsRepository.schema.author_email: "email2@email.com",
         CompaniesContributorsRepository.schema.company: "Company1",
         CompaniesContributorsRepository.schema.commits: 73,
         CompaniesContributorsRepository.schema.license: "other",
         CompaniesContributorsRepository.schema.repository: "repo/name",
         CompaniesContributorsRepository.schema.language: "python",
         CompaniesContributorsRepository.schema.date: datetime(year=2021, month=1, day=1)
         },
        {CompaniesContributorsRepository.schema.author_name: "Author Name2",
         CompaniesContributorsRepository.schema.author_email: "email2@email.com",
         CompaniesContributorsRepository.schema.company: "Company2",
         CompaniesContributorsRepository.schema.commits: 73,
         CompaniesContributorsRepository.schema.license: "other",
         CompaniesContributorsRepository.schema.repository: "ya-repo/name",
         CompaniesContributorsRepository.schema.language: "python",
         CompaniesContributorsRepository.schema.date: datetime(year=2021, month=1, day=1)
         },
        {CompaniesContributorsRepository.schema.author_name: "Author Name3",
         CompaniesContributorsRepository.schema.author_email: "email3@email.com",
         CompaniesContributorsRepository.schema.company: "Company2",
         CompaniesContributorsRepository.schema.commits: 128,
         CompaniesContributorsRepository.schema.license: "other",
         CompaniesContributorsRepository.schema.repository: "repo/name",
         CompaniesContributorsRepository.schema.language: "python",
         CompaniesContributorsRepository.schema.date: datetime(year=2021, month=1, day=1)
         },
    ])


@pytest.fixture()
def expected():
    return pd.DataFrame([
        {NumberOfCompaniesCommitsInRepositories.company: "Company1",
         NumberOfCompaniesCommitsInRepositories.repository: 'repo/name',
         NumberOfCompaniesCommitsInRepositories.commits: 115},
        {NumberOfCompaniesCommitsInRepositories.company: "Company2",
         NumberOfCompaniesCommitsInRepositories.repository: 'repo/name',
         NumberOfCompaniesCommitsInRepositories.commits: 128},
        {NumberOfCompaniesCommitsInRepositories.company: "Company2",
         NumberOfCompaniesCommitsInRepositories.repository: 'ya-repo/name',
         NumberOfCompaniesCommitsInRepositories.commits: 73},
    ])


def test_get_num_companies_commits_per_repo(mocker, comp_contrib_repos_complex_df, load_date,
                                            expected):
    mocker.patch("osci.datalake.CompaniesContributorsRepository.read", return_value=comp_contrib_repos_complex_df)
    res = get_num_companies_commit_per_repository(load_date)
    assert_frame_equal(res, expected)
