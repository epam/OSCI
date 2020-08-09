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


def get_repos_commits_amount(df: DataFrame,
                             repo_name_field: str,
                             commits_id_field: str,
                             result_field: str = 'Commits') -> DataFrame:
    """Get amount of repos commits

    :param df: PushEventsCommits
    :param repo_name_field: Repository name field
    :param commits_id_field: Commit identifier (such as SHA)
    :param result_field: Field in output df which must contains amount of commits
    :return:
    """
    return df.select(repo_name_field, commits_id_field) \
        .groupBy(repo_name_field) \
        .agg(f.count(f.col(commits_id_field)).alias(result_field)) \
        .sort(result_field, ascending=False)


def get_employees_repos_commits_amount(df: DataFrame,
                                       repo_name_field: str,
                                       author_name_field: str,
                                       author_email_field: str,
                                       commits_id_field: str,
                                       result_field: str = 'Commits') -> DataFrame:
    """Get amount of employees' repos commits

    :param df: PushEventsCommits
    :param repo_name_field: Repository name field
    :param author_name_field: Commit author name field
    :param author_email_field: Commit author email field
    :param commits_id_field: Commit identifier (such as SHA)
    :param result_field: Field in output df which must contains amount of commits
    :return:
    """
    return df.select(repo_name_field, author_name_field, author_email_field, commits_id_field) \
        .groupBy(repo_name_field, author_name_field, author_email_field) \
        .agg(f.count(f.col(commits_id_field)).alias(result_field)) \
        .sort(result_field, ascending=False)
