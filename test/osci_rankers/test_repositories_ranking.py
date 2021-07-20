import pytest
import datetime

from pyspark.sql import Row
from osci.transformers.rankers.repositories_ranking import get_repos_commits_amount, get_employees_repos_commits_amount


@pytest.fixture()
def commits(spark_session):
    return spark_session.createDataFrame([
        Row(sha='0', company='Google', author='Googler 1', author_email='googler_1@google.com',
            date=datetime.datetime(year=2019, month=11, day=3), repo='repo_google1'),
        Row(sha='1', company='Google', author='Googler 1', author_email='googler_1@google.com',
            date=datetime.datetime(year=2020, month=11, day=3), repo='repo_google2'),
        Row(sha='2', company='Google', author='Googler 1', author_email='googler_1@google.com',
            date=datetime.datetime(year=2020, month=11, day=3), repo='repo_google2'),
        Row(sha='3', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2019, month=11, day=3), repo='repo_google2'),
        Row(sha='4', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2019, month=11, day=3), repo='repo_google2'),
        Row(sha='5', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2020, month=12, day=3), repo='repo_google2'),
        Row(sha='6', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2020, month=12, day=3), repo='repo_google2'),
        Row(sha='7', company='Google', author='Googler 2', author_email='googler_2@google.com',
            date=datetime.datetime(year=2020, month=12, day=3), repo='repo_google2'),
        Row(sha='8', company='Google', author='Googler 3', author_email='googler_3@google.com',
            date=datetime.datetime(year=2020, month=12, day=3), repo='repo_google2'),
        Row(sha='9', company='Google', author='Googler 3', author_email='googler_3@google.com',
            date=datetime.datetime(year=2020, month=12, day=3), repo='repo_google2'),
        Row(sha='10', company='Google', author='Googler 3', author_email='googler_3@google.com',
            date=datetime.datetime(year=2020, month=12, day=3), repo='repo_google2'),
        Row(sha='11', company='Google', author='Googler 3', author_email='googler_3@google.com',
            date=datetime.datetime(year=2020, month=12, day=3), repo='repo_google2'),
        Row(sha='12', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3), repo='repo_epam1'),
        Row(sha='13', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3), repo='repo_epam1'),
        Row(sha='14', company='Epam', author='Epamer 1', author_email='epamer_1@epam.com',
            date=datetime.datetime(year=2020, month=10, day=3), repo='repo_epam1')
    ])


def test_get_repos_commits_amount(commits):
    df = get_repos_commits_amount(df=commits,repo_name_field='repo', commits_id_field='sha', result_field='commits')
    test_case = [
        ('repo_google2', 11),
        ('repo_epam1', 3),
        ('repo_google1', 1),
    ]
    assert [(row.repo, row.commits) for row in df.collect()] == test_case


def test_get_employees_repos_commits_amount(commits):
    df = get_employees_repos_commits_amount(df=commits,
                                            repo_name_field='repo',
                                            author_name_field='author',
                                            author_email_field='author_email',
                                            commits_id_field='sha',
                                            result_field='commits')
    test_case = [
        ('repo_google2', 'Googler 2', 'googler_2@google.com', 5),
        ('repo_google2', 'Googler 3', 'googler_3@google.com', 4),
        ('repo_epam1', 'Epamer 1', 'epamer_1@epam.com', 3),
        ('repo_google2', 'Googler 1', 'googler_1@google.com', 2),
        ('repo_google1', 'Googler 1', 'googler_1@google.com', 1),

    ]
    assert [(row.repo, row.author, row.author_email, row.commits) for row in df.collect()] == test_case
