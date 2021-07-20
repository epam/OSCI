import pyspark
import pytest
import pandas as pd

from osci.datalake import DataLake


@pytest.fixture(scope='session', autouse=True)
def spark_context():
    conf = pyspark.conf.SparkConf()
    conf.setMaster('local[*]')
    sc = pyspark.SparkContext.getOrCreate(conf=conf)
    yield sc
    sc.stop()


@pytest.fixture(scope='session')
def spark_session(spark_context: pyspark.SparkContext):
    return pyspark.sql.SparkSession.builder.config('spark.sql.shuffle.partitions', spark_context.defaultParallelism) \
        .getOrCreate()


@pytest.fixture(scope='session')
def staging_repository_df():
    return pd.DataFrame([
        {DataLake().staging.schemas.repositories.name: "epam/OSCI",
         DataLake().staging.schemas.repositories.language: "Python",
         DataLake().staging.schemas.repositories.license: "gpl-3.0",
         DataLake().staging.schemas.repositories.downloaded_at: "2021-01-01"},
    ])


@pytest.fixture(scope='session')
def raw_push_events_commit_df():
    return pd.DataFrame([
        {DataLake().staging.schemas.push_commits.event_id: "1111111",
         DataLake().staging.schemas.push_commits.event_created_at: "2021-01-01 00:15:22+00:00",
         DataLake().staging.schemas.push_commits.actor_login: "actor_login",
         DataLake().staging.schemas.push_commits.repo_name: "epam/OSCI",
         DataLake().staging.schemas.push_commits.org_name: 'EPAM',
         DataLake().staging.schemas.push_commits.sha: "aaa656b0d05ec5b8ed5beb2f94c4aa11ea111a1a",
         DataLake().staging.schemas.push_commits.author_name: "User Name",
         DataLake().staging.schemas.push_commits.author_email: "17ea111d7a46effe1111b086213468b8b31643bf@epam.com",
         DataLake().staging.schemas.push_commits.company: "EPAM"
         },])


@pytest.fixture(scope='session')
def staging_push_event_commit_df():
    return pd.DataFrame([
        {DataLake().staging.schemas.push_commits.event_id: "1111111",
         DataLake().staging.schemas.push_commits.event_created_at: "2021-01-01 00:15:22+00:00",
         DataLake().staging.schemas.push_commits.actor_login: "actor_login",
         DataLake().staging.schemas.push_commits.repo_name: "epam/OSCI",
         DataLake().staging.schemas.push_commits.org_name: 'EPAM',
         DataLake().staging.schemas.push_commits.sha: "aaa656b0d05ec5b8ed5beb2f94c4aa11ea111a1a",
         DataLake().staging.schemas.push_commits.author_name: "User Name",
         DataLake().staging.schemas.push_commits.author_email: "17ea111d7a46effe1111b086213468b8b31643bf@epam.com",
         DataLake().staging.schemas.push_commits.company: "EPAM",
         DataLake().staging.schemas.push_commits.language: "Python",
         DataLake().staging.schemas.push_commits.license: "gpl-3.0"
         }])
