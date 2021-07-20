import pytest
import datetime

from pyspark.sql import Row
from pyspark.sql import functions as f
from osci.transformers.rankers.employees_ranking import get_companies_employees_activity_rank_combined, \
    CommitsThresholds, get_amount_employees_monthly, get_companies_rank_by_employees_amount


@pytest.fixture()
def commits(spark_session):
    return spark_session.createDataFrame([
        Row(sha='1', company='Google', author='Googler 1', author_email='googler_1@google.com', date=datetime.datetime(year=2019, month=11, day=3)),
        Row(sha='2', company='Google', author='Googler 1', author_email='googler_1@google.com', date=datetime.datetime(year=2020, month=11, day=3)),
        Row(sha='3', company='Google', author='Googler 2', author_email='googler_2@google.com', date=datetime.datetime(year=2019, month=11, day=3)),
        Row(sha='4', company='Google', author='Googler 2', author_email='googler_2@google.com', date=datetime.datetime(year=2020, month=11, day=3)),
        Row(sha='5', company='Google', author='Googler 3', author_email='googler_3@google.com', date=datetime.datetime(year=2020, month=11, day=3)),
        Row(sha='6', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com', date=datetime.datetime(year=2020, month=11, day=3)),
        Row(sha='7', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com', date=datetime.datetime(year=2020, month=11, day=3)),
        Row(sha='9', company='Epam', author='Epamer 2', author_email='epamer_2@epam.com', date=datetime.datetime(year=2020, month=11, day=3)),
        Row(sha='10', company='Alibaba', author='Alibaber 1', author_email='alibaber_1@ali.com', date=datetime.datetime(year=2020, month=11, day=3)),
    ])


def test_companies_employees_activity_rank_combined(commits):
    thresholds = [
        CommitsThresholds(col='gte1', threshold=1),
        CommitsThresholds(col='gte2', threshold=2)
    ]
    df = get_companies_employees_activity_rank_combined(df=commits,
                                                        commits_id_field='sha',
                                                        author_email_field='author_email',
                                                        company_field='company',
                                                        commits_thresholds=thresholds,
                                                        order_by_field=thresholds[1].col)
    test_case = [
        ('Google', 3, 2),
        ('Epam', 2, 1),
        ('Alibaba', 1, None),
    ]
    assert [(row.company, row.gte1, row.gte2) for row in df.collect()] == test_case


def test_get_amount_employees_monthly(commits):
    df = get_amount_employees_monthly(df=commits.filter(f.col('company') == 'Google'),
                                      author_email_field='author_email',
                                      datetime_field='date',
                                      result_employee_field='employees',
                                      result_month_field='month')
    test_case = [
        ('2019-11', 2),
        ('2020-11', 3),
    ]
    assert [(row.month, row.employees) for row in df.collect()] == test_case


def test_get_companies_rank_by_employees_amount(commits):
    df = get_companies_rank_by_employees_amount(df=commits,
                                                company_field='company',
                                                author_email_field='author_email',
                                                result_employee_field='employees')
    test_case = [
        ('Google', 3),
        ('Epam', 2),
        ('Alibaba', 1),
    ]
    assert [(row.company, row.employees) for row in df.collect()] == test_case
