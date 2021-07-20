import pytest
import datetime

from pyspark.sql import Row
from osci.datalake.schemas.staging import PushEventsCommitsSchema
from osci.transformers.licenses import get_licenses_commits


@pytest.fixture()
def raw_commits(spark_session):
    return spark_session.createDataFrame([
        Row(sha='1', company='Google', author='Googler 1', author_email='googler_1@google.com',
            date=datetime.datetime(year=2019, month=11, day=3), license="apache-2.0"),
        Row(sha='2', company='Google', author='Googler 1', author_email='googler_1@google.com',
            date=datetime.datetime(year=2020, month=11, day=3), license="apache-2.0"),
        Row(sha='3', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2019, month=11, day=3), license="mit"),
        Row(sha='4', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2020, month=12, day=3), license="mit"),
        Row(sha='5', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3), license="apache-2.0"),
        Row(sha='6', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3), license="apache-2.0"),
        Row(sha='7', company='Epam', author='Epamer 2', author_email='epamer_2@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3), license="apache-2.0"),
        Row(sha='8', company='Alibaba', author='Alibaber 1', author_email='alibaber_1@ali.com',
            date=datetime.datetime(year=2020, month=9, day=3), license="lgpl-2.1"),
    ])


@pytest.fixture()
def expected_licensed_commits(spark_session):
    return [
        ('Alibaba', 'lgpl-2.1', 1),
        ('Epam', 'apache-2.0', 3),
        ('Google', 'apache-2.0', 2),
        ('Google', 'mit', 2)
    ]


def test_transform_osci_licenses(raw_commits, expected_licensed_commits):
    df = get_licenses_commits(df=raw_commits,
                              company=PushEventsCommitsSchema.company,
                              license=PushEventsCommitsSchema.license,
                              commits_id_field=PushEventsCommitsSchema.sha,
                              result_field='commits')

    assert sorted([(row.company, row.license, row.commits) for row in df.collect()],
                  key=lambda x: (x[0], x[1])) == expected_licensed_commits
