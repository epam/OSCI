import pytest
import datetime

from pyspark.sql import Row
from osci.transformers.rankers.commits_ranking import (
    get_commits_ranking,
    get_month_by_month_commits_amounts,
)


@pytest.fixture()
def commits(spark_session):
    return spark_session.createDataFrame([
        Row(sha='1', company='Google', author='Googler 1', author_email='googler_1@google.com',
            date=datetime.datetime(year=2019, month=11, day=3)),
        Row(sha='2', company='Google', author='Googler 1', author_email='googler_1@google.com',
            date=datetime.datetime(year=2020, month=11, day=3)),
        Row(sha='3', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2019, month=11, day=3)),
        Row(sha='4', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2020, month=12, day=3)),
        Row(sha='5', company='Google', author='Googler 3', author_email='googler_3@google.com',
            date=datetime.datetime(year=2020, month=12, day=3)),
        Row(sha='6', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3)),
        Row(sha='7', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3)),
        Row(sha='9', company='Epam', author='Epamer 2', author_email='epamer_2@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3)),
        Row(sha='10', company='Alibaba', author='Alibaber 1', author_email='alibaber_1@ali.com',
            date=datetime.datetime(year=2020, month=9, day=3)),
    ])


def test_get_commits_ranking(commits):
    df = get_commits_ranking(df=commits,
                             commits_id_field='sha',
                             company_field='company',
                             result_field='commits')
    test_case = [
        ('Google', 5),
        ('Epam', 3),
        ('Alibaba', 1),
    ]
    assert [(row.company, row.commits) for row in df.collect()] == test_case


def test_get_month_by_month_commits_amounts(commits):
    df = get_month_by_month_commits_amounts(df=commits,
                                            commits_id_field='sha',
                                            datetime_field='date',
                                            result_field='commits',
                                            result_month_field='month')
    test_case = [
        ('2019-11', 2),
        ('2020-09', 1),
        ('2020-10', 3),
        ('2020-11', 1),
        ('2020-12', 2),
    ]
    assert [(row.month, row.commits) for row in df.collect()] == test_case
