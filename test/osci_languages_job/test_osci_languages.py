import pytest
import datetime

from pyspark.sql import Row
from osci.datalake.schemas.staging import PushEventsCommitsSchema
from osci.transformers.languages import get_languages_commits


@pytest.fixture()
def raw_commits(spark_session):
    return spark_session.createDataFrame([
        Row(sha='1', company='Google', author='Googler 1', author_email='googler_1@google.com',
            date=datetime.datetime(year=2019, month=11, day=3), language="python"),
        Row(sha='2', company='Google', author='Googler 1', author_email='googler_1@google.com',
            date=datetime.datetime(year=2020, month=11, day=3), language="python"),
        Row(sha='3', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2019, month=11, day=3), language="c"),
        Row(sha='4', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2020, month=12, day=3), language="c"),
        Row(sha='5', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3), language="python"),
        Row(sha='6', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3), language="python"),
        Row(sha='7', company='Epam', author='Epamer 2', author_email='epamer_2@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3), language=None),
        Row(sha='8', company='Alibaba', author='Alibaber 1', author_email='alibaber_1@ali.com',
            date=datetime.datetime(year=2020, month=9, day=3), language="javascript"),
    ])


@pytest.fixture()
def expected_language_commits(spark_session):
    return [
        ('Alibaba', 'javascript', 1),
        ('Epam', 'python', 2),
        ('Google', 'c', 2),
        ('Google', 'python', 2)
    ]


def test_transform_osci_languages(raw_commits, expected_language_commits):
    df = get_languages_commits(df=raw_commits,
                               company=PushEventsCommitsSchema.company,
                               language=PushEventsCommitsSchema.language,
                               commits_id_field=PushEventsCommitsSchema.sha,
                               result_field='commits')
    assert sorted([(row.company, row.language, row.commits) for row in df.collect()],
                  key=lambda x: (x[0], x[1])) == expected_language_commits
