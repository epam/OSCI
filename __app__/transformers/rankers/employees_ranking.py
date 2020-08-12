"""Copyright since 2019, EPAM Systems

   This file is part of OSCI.

   OSCI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   OSCI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>."""

from typing import List, NamedTuple
from functools import reduce

from pyspark.sql import DataFrame
from pyspark.sql import functions as f


class CommitsThresholds(NamedTuple):
    """Commits thresholds"""
    col: str  # Result column name
    threshold: int


DEFAULT_THRESHOLDS = (
    CommitsThresholds(col='Commits >= 1', threshold=1),
    CommitsThresholds(col='Commits >= 10', threshold=10)
)


def get_companies_employees_activity(df: DataFrame, commits_id_field: str, author_email_field: str,
                                     company_field: str, result_field: str = 'Commits') -> DataFrame:
    """Get companies employees activity by amount of commits

    :param df: PushEventsCommits
    :param commits_id_field: Commit identifier field (ex. 'sha')
    :param author_email_field: Commit author email field
    :param company_field: Company name field
    :param result_field: Field in output df which must contains amount of commits
    :return:
    """
    return df \
        .select(f.col(commits_id_field), f.col(author_email_field), f.col(company_field)) \
        .groupBy(author_email_field, company_field) \
        .agg(f.count(f.col(commits_id_field)).alias(result_field))


def get_companies_employees_activity_rank_combined(df: DataFrame, commits_id_field: str,
                                                   author_email_field: str, company_field: str,
                                                   commits_thresholds: List[CommitsThresholds] = DEFAULT_THRESHOLDS,
                                                   order_by_field: str = DEFAULT_THRESHOLDS[1].col) -> DataFrame:
    """Get companies rank by employees activity (amount of commits)

    :param df: PushEventsCommits
    :param commits_id_field: Commit identifier field (ex. 'sha')
    :param author_email_field: Commit author email field
    :param company_field: Company name field
    :param commits_thresholds: Commits thresholds (ex.: [CommitsThresholds(col='Commits >= 10', threshold=10)])
    :param order_by_field: Result order by field
    :return:
    """
    if not len(commits_thresholds):
        raise ValueError(f'Param commits_thresholds must be non empty. Passed: {commits_thresholds}')
    commits_count_field = 'Commits'
    employees_activity = get_companies_employees_activity(df=df,
                                                          commits_id_field=commits_id_field,
                                                          author_email_field=author_email_field,
                                                          company_field=company_field,
                                                          result_field=commits_count_field).cache()

    return reduce(
        lambda df1, df2: df1.join(df2, on=company_field, how='left'),
        [
            employees_activity.filter(
                f.col(commits_count_field) >= commits_threshold.threshold
            ).select(
                company_field, author_email_field
            ).groupBy(
                f.col(company_field)
            ).agg(
                f.count(f.col(author_email_field)).alias(commits_threshold.col)
            )
            for commits_threshold in commits_thresholds
        ]
    ).sort(order_by_field, ascending=False)


def get_companies_rank_by_employees_amount(df: DataFrame,
                                           company_field: str,
                                           author_email_field: str,
                                           result_employee_field: str = 'Employees') -> DataFrame:
    """Get companies ranking by amount of employees

    :param df: PushEventsCommits
    :param company_field: Company name field
    :param author_email_field: Commit author email field
    :param result_employee_field: Field in output df which must contains amount of employees
    :return:
    """
    return df \
        .select(company_field, author_email_field) \
        .groupBy(company_field) \
        .agg(f.countDistinct(f.col(author_email_field)).alias(result_employee_field)) \
        .sort(result_employee_field, ascending=False)


def get_amount_employees_monthly(df: DataFrame,
                                 author_email_field: str,
                                 datetime_field: str,
                                 result_employee_field: str = 'Employees',
                                 result_month_field: str = 'Month') -> DataFrame:
    """Get amount of employees (that have any activity) monthly for company

    :param df: PushEventsCommits
    :param author_email_field: Commit author email field
    :param datetime_field: Event created at datetime field
    :param result_employee_field: Field in output df which must contains amount of employees
    :param result_month_field: Field in output df which must contains month
    :return:
    """
    return df.select(author_email_field, datetime_field) \
        .withColumn(result_month_field, f.date_format(datetime_field, "yyyy-MM")) \
        .select(author_email_field, result_month_field) \
        .groupBy(result_month_field) \
        .agg(f.count(f.col(author_email_field)).alias(result_employee_field)) \
        .sort(result_month_field)



