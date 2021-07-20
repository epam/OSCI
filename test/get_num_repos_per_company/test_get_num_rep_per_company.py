import pandas as pd
import pytest
from datetime import datetime
from osci.postprocess.get_num_repos_per_company import get_num_repos_per_company
from osci.datalake.schemas.public import NumberRepositoryPerCompaniesSchema
from pandas._testing import assert_frame_equal
from osci.datalake import CompaniesContributorsRepository


@pytest.fixture()
def num_per_per_comp_single_expected():
    return pd.DataFrame([
        {NumberRepositoryPerCompaniesSchema.company: "Company",
         NumberRepositoryPerCompaniesSchema.repository: 1}
    ])


@pytest.fixture()
def comp_contrib_repos_complex_df():
    return pd.DataFrame([
        {CompaniesContributorsRepository.schema.author_name: "Author Name",
         CompaniesContributorsRepository.schema.author_email: "email@email.com",
         CompaniesContributorsRepository.schema.company: "Company1",
         CompaniesContributorsRepository.schema.commits: 11111,
         CompaniesContributorsRepository.schema.license: "other",
         CompaniesContributorsRepository.schema.repository: "repo/name",
         CompaniesContributorsRepository.schema.language: "python",
         CompaniesContributorsRepository.schema.date: datetime(year=2021, month=1, day=1)
         },
        {CompaniesContributorsRepository.schema.author_name: "Author Name2",
         CompaniesContributorsRepository.schema.author_email: "email2@email.com",
         CompaniesContributorsRepository.schema.company: "Company2",
         CompaniesContributorsRepository.schema.commits: 22222,
         CompaniesContributorsRepository.schema.license: "other",
         CompaniesContributorsRepository.schema.repository: "repo/name",
         CompaniesContributorsRepository.schema.language: "python",
         CompaniesContributorsRepository.schema.date: datetime(year=2021, month=1, day=1)
         },
        {CompaniesContributorsRepository.schema.author_name: "Author Name3",
         CompaniesContributorsRepository.schema.author_email: "email3@email.com",
         CompaniesContributorsRepository.schema.company: "Company2",
         CompaniesContributorsRepository.schema.commits: 33333,
         CompaniesContributorsRepository.schema.license: "other",
         CompaniesContributorsRepository.schema.repository: "repo/name",
         CompaniesContributorsRepository.schema.language: "python",
         CompaniesContributorsRepository.schema.date: datetime(year=2021, month=1, day=1)
         },
    ])


@pytest.fixture()
def num_per_per_comp_complex_expected():
    return pd.DataFrame([
        {NumberRepositoryPerCompaniesSchema.company: "Company1",
         NumberRepositoryPerCompaniesSchema.repository: 1},
        {NumberRepositoryPerCompaniesSchema.company: "Company2",
         NumberRepositoryPerCompaniesSchema.repository: 2},
    ])


def test_num_per_per_companies_success(mocker, comp_contrib_repos_complex_df, load_date,
                                       num_per_per_comp_complex_expected):
    mocker.patch("osci.datalake.CompaniesContributorsRepository.read", return_value=comp_contrib_repos_complex_df)
    res = get_num_repos_per_company(load_date)
    assert_frame_equal(res, num_per_per_comp_complex_expected)
