"""Copyright since 2020, EPAM Systems

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

from pyspark.sql import DataFrame
from pyspark.sql import functions as f


def get_commits_ranking(df: DataFrame, commits_id_field: str, company_field: str,
                        result_field: str = 'Commits') -> DataFrame:
    """Get company amount of commits

    :param df: PushEventsCommits

    :param commits_id_field: Commit identifier (such as SHA)
    :param company_field: Company name field

    :param result_field: Field in output df which must contains amount of commits
    :return:
    """
    return df \
        .select(f.col(commits_id_field), f.col(company_field)) \
        .groupBy(company_field) \
        .agg(f.count(commits_id_field).alias(result_field)) \
        .sort(result_field, ascending=False)


def get_month_by_month_commits_amounts(df: DataFrame, commits_id_field: str, datetime_field: str,
                                       result_month_field: str = 'Month',
                                       result_field: str = 'Commits'):
    """Get month-by-month amount of commits

    :param df: PushEventsCommits

    :param commits_id_field: Commit identifier (such as SHA)
    :param datetime_field: Event created at datetime field

    :param result_month_field: Field in output df which must contains month
    :param result_field: Field in output df which must contains amount of commits
    :return:
    """
    return df \
        .select(f.col(commits_id_field), f.col(datetime_field)) \
        .groupby(f.date_format(f.col(datetime_field), "yyyy-MM").alias(result_month_field)) \
        .agg(f.count('*').alias(result_field)) \
        .sort(result_month_field)


def get_employees_commits_amount(df: DataFrame,
                                 author_name_field: str,
                                 author_email_field: str,
                                 commits_id_field: str,
                                 result_field: str = 'Commits') -> DataFrame:
    """Get amount of employees' commits

    :param df: PushEventsCommits
    :param author_name_field: Commit author name field
    :param author_email_field: Commit author email field
    :param commits_id_field: Commit identifier (such as SHA)
    :param result_field: Field in output df which must contains amount of commits
    :return:
    """
    return df.select(author_name_field, author_email_field, commits_id_field) \
        .groupBy(author_name_field, author_email_field) \
        .agg(f.count(f.col(commits_id_field)).alias(result_field)) \
        .sort(result_field, ascending=False)
