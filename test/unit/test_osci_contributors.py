import pytest
import datetime

from pyspark.sql import Row

from osci.transformers.contributors import get_osci_contributors


@pytest.fixture()
def commits(spark_session):
    return spark_session.createDataFrame([
        Row(sha='debb9e28', company='Google', author='conubia', author_email='conubia@google.com'),
        Row(sha='6103c952', company='Google', author='conubia', author_email='conubia@google.com'),
        Row(sha='23c55e5f', company='Google', author='conubia', author_email='conubia@google.com'),
        Row(sha='5b154a70', company='Google', author='conubia', author_email='conubia@google.com'),
        Row(sha='d7a799a1', company='Google', author='conubia', author_email='conubia@google.com'),
        Row(sha='a1c16e24', company='Google', author='lorem', author_email='lorem@google.com'),
        Row(sha='fd265639', company='Google', author='lorem', author_email='lorem@google.com'),
        Row(sha='d5d99d4a', company='Google', author='lorem', author_email='lorem@google.com'),
        Row(sha='542487a2', company='Google', author='lorem', author_email='lorem@google.com'),
        Row(sha='deefbeff', company='Google', author='taciti', author_email='taciti@google.com'),
        Row(sha='b8202070', company='Google', author='taciti', author_email='taciti@google.com'),
        Row(sha='ea85cf67', company='Google', author='taciti', author_email='taciti@google.com'),
        Row(sha='44f54bf9', company='Google', author='ad', author_email='ad@google.com'),
        Row(sha='5c4a91c7', company='Google', author='ad', author_email='ad@google.com'),
        Row(sha='c01a2c5c', company='Microsoft', author='sociosqu', author_email='sociosqu@microsoft.com'),
        Row(sha='79880485', company='Microsoft', author='sociosqu', author_email='sociosqu@microsoft.com'),
        Row(sha='88c3877d', company='Microsoft', author='sociosqu', author_email='sociosqu@microsoft.com'),
        Row(sha='6bc7c62e', company='Microsoft', author='sociosqu', author_email='sociosqu@microsoft.com'),
        Row(sha='0a35957b', company='Microsoft', author='sociosqu', author_email='sociosqu@microsoft.com'),
        Row(sha='f58e153e', company='Microsoft', author='lectus', author_email='lectus@microsoft.com'),
        Row(sha='e3f9c4f3', company='Microsoft', author='lectus', author_email='lectus@microsoft.com'),
        Row(sha='756e87ec', company='Microsoft', author='lectus', author_email='lectus@microsoft.com'),
        Row(sha='5d51fdf4', company='Microsoft', author='lectus', author_email='lectus@microsoft.com'),
        Row(sha='9b93972a', company='Microsoft', author='morbi', author_email='morbi@microsoft.com'),
        Row(sha='573824a0', company='Microsoft', author='morbi', author_email='morbi@microsoft.com'),
        Row(sha='7e701ecf', company='Microsoft', author='morbi', author_email='morbi@microsoft.com'),
        Row(sha='997ef4ee', company='EPAM', author='eu', author_email='eu@epam.com'),
        Row(sha='74fe5117', company='EPAM', author='eu', author_email='eu@epam.com'),
        Row(sha='49ae924a', company='EPAM', author='eu', author_email='eu@epam.com'),
        Row(sha='1d4c047f', company='EPAM', author='eu', author_email='eu@epam.com'),
        Row(sha='21c3bf70', company='EPAM', author='eu', author_email='eu@epam.com'),
        Row(sha='87a70508', company='EPAM', author='varius', author_email='varius@epam.com'),
        Row(sha='02510721', company='EPAM', author='varius', author_email='varius@epam.com'),
        Row(sha='3b100c4b', company='EPAM', author='varius', author_email='varius@epam.com'),
        Row(sha='58866ad5', company='EPAM', author='varius', author_email='varius@epam.com'),
    ])


def test_get_osci_contributors(commits):
    limit = 3
    df = get_osci_contributors(df=commits,
                               author_name_field='author',
                               author_email_field='author_email',
                               company_field='company',
                               commits_id_field='sha',
                               result_field='commits',
                               limit=limit)

    test_case = [
        ('Google', 'conubia', 'conubia@google.com', 5),
        ('Google', 'lorem', 'lorem@google.com', 4),
        ('Google', 'taciti', 'taciti@google.com', 3),
        ('Microsoft', 'sociosqu', 'sociosqu@microsoft.com', 5),
        ('Microsoft', 'lectus', 'lectus@microsoft.com', 4),
        ('Microsoft', 'morbi', 'morbi@microsoft.com', 3),
        ('EPAM', 'eu', 'eu@epam.com', 5),
        ('EPAM', 'varius', 'varius@epam.com', 4),
    ]

    assert [(row.company, row.author, row.author_email, row.commits) for row in df.collect()] == test_case
