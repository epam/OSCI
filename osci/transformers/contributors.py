"""Copyright since 2021, EPAM Systems

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

from pyspark.sql import DataFrame, Window, functions as f


def get_osci_contributors(df: DataFrame,
                          author_name_field: str,
                          author_email_field: str,
                          company_field: str,
                          commits_id_field: str,
                          result_field: str = 'Commits',
                          limit: int = 5) -> DataFrame:
    """Get top of contributors for each company

    :param df: PushEventsCommits

    :param author_name_field: Commit author name field
    :param author_email_field: Commit author email field
    :param commits_id_field: Commit identifier (such as SHA)
    :param company_field: Company name field

    :param limit: Limit of contributors for company (top size)

    :param result_field: Field in output df which must contains amount of commits
    :return:
    """
    window = Window \
        .partitionBy(f.col(company_field)) \
        .orderBy(f.col(result_field).desc())

    return df \
        .select(f.col(company_field), f.col(author_name_field), f.col(author_email_field), f.col(commits_id_field)) \
        .groupBy(company_field, author_name_field, author_email_field) \
        .agg(f.count(commits_id_field).alias(result_field)) \
        .select(f.col('*'), f.row_number().over(window).alias('row_number')) \
        .where(f.col('row_number') <= limit).drop(f.col('row_number'))
