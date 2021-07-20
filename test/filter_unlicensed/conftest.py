import pytest
import pandas as pd

from osci.datalake import DataLake


@pytest.fixture()
def no_match_license_raw_push_event_commit_df():
    return pd.DataFrame([
        {DataLake().staging.schemas.push_commits.event_id: "222222",
         DataLake().staging.schemas.push_commits.event_created_at: "2021-01-01 00:15:22+00:00",
         DataLake().staging.schemas.push_commits.actor_login: "actor_login",
         DataLake().staging.schemas.push_commits.repo_name: "test/TEST",
         DataLake().staging.schemas.push_commits.org_name: None,
         DataLake().staging.schemas.push_commits.sha: "bbb656b0d05ec5b8ed5beb2f94c4aa11ea111a1a",
         DataLake().staging.schemas.push_commits.author_name: "User Name",
         DataLake().staging.schemas.push_commits.author_email: "17ea111d7a46effe1111b086213468b8b31643bf@epam.com",
         DataLake().staging.schemas.push_commits.company: "EPAM"
         }])


@pytest.fixture()
def abnormal_staging_repository_df():
    return pd.DataFrame([
        {DataLake().staging.schemas.repositories.name: "epam/OSCI",
         DataLake().staging.schemas.repositories.language: "Python",
         DataLake().staging.schemas.repositories.license: "gpl-3.0",
         DataLake().staging.schemas.repositories.downloaded_at: "2021-01-01"},
        {DataLake().staging.schemas.repositories.name: "not_exist/REPOSITORY",
         DataLake().staging.schemas.repositories.language: "Python",
         DataLake().staging.schemas.repositories.license: "gpl-3.0",
         DataLake().staging.schemas.repositories.downloaded_at: "2021-01-01"},
    ])


@pytest.fixture()
def unfiltered_raw_push_events_commit_df():
    return pd.DataFrame([
        {DataLake().staging.schemas.push_commits.event_id: "222222",
         DataLake().staging.schemas.push_commits.event_created_at: "2021-01-01 00:15:22+00:00",
         DataLake().staging.schemas.push_commits.actor_login: "actor_login",
         DataLake().staging.schemas.push_commits.repo_name: "unfiltered/REPOSITORY",
         DataLake().staging.schemas.push_commits.org_name: "EPAM",
         DataLake().staging.schemas.push_commits.sha: "bbb656b0d05ec5b8ed5beb2f94c4aa11ea111a1a",
         DataLake().staging.schemas.push_commits.author_name: "User Name",
         DataLake().staging.schemas.push_commits.author_email: "17ea111d7a46effe1111b086213468b8b31643bf@epam.com",
         DataLake().staging.schemas.push_commits.company: "EPAM"
         },
        {DataLake().staging.schemas.push_commits.event_id: "1111111",
         DataLake().staging.schemas.push_commits.event_created_at: "2021-01-01 00:15:22+00:00",
         DataLake().staging.schemas.push_commits.actor_login: "actor_login",
         DataLake().staging.schemas.push_commits.repo_name: "epam/OSCI",
         DataLake().staging.schemas.push_commits.org_name: 'EPAM',
         DataLake().staging.schemas.push_commits.sha: "aaa656b0d05ec5b8ed5beb2f94c4aa11ea111a1a",
         DataLake().staging.schemas.push_commits.author_name: "User Name",
         DataLake().staging.schemas.push_commits.author_email: "17ea111d7a46effe1111b086213468b8b31643bf@epam.com",
         DataLake().staging.schemas.push_commits.company: "EPAM"
         }
    ])


@pytest.fixture()
def filter_columns():
    return [DataLake().staging.schemas.repositories.license]


@pytest.fixture()
def adjunct_columns():
    return [
        DataLake().staging.schemas.repositories.name,
        DataLake().staging.schemas.repositories.language,
        DataLake().staging.schemas.repositories.license
    ]


@pytest.fixture()
def required_columns():
    return DataLake().staging.schemas.push_commits.required


@pytest.fixture()
def right_index():
    return DataLake().staging.schemas.repositories.name


@pytest.fixture()
def left_index():
    return DataLake().staging.schemas.push_commits.repo_name