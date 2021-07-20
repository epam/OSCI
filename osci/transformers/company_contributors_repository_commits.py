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

from pyspark.sql import DataFrame
from pyspark.sql import functions as f

from datetime import date


def get_company_contributors_repository_commits(df: DataFrame,
                                                author_name_field: str,
                                                author_email_field: str,
                                                repo_name_field: str,
                                                language_field: str,
                                                license_field: str,
                                                company_field: str,
                                                commits_id_field: str,
                                                datetime_field: str,
                                                day: date,
                                                result_field: str = 'Commits') -> DataFrame:
    """Get company contributors repository commits

    :param df: PushEventsCommits

    :param author_name_field: Commit author name field
    :param author_email_field: Commit author email field
    :param repo_name_field: Repository name field
    :param language_field: Language field
    :param license_field: License field
    :param datetime_field: Event created at datetime field
    :param day: Date of filtration
    :param commits_id_field: Commit identifier (such as SHA)
    :param company_field: Company name field

    :param result_field: Field in output df which must contains amount of commits
    :return:
    """
    return df \
        .select(f.col(author_name_field), f.col(author_email_field),
                f.col(repo_name_field), f.col(language_field),
                f.col(license_field), f.col(company_field),
                f.col(commits_id_field), f.col(datetime_field)) \
        .filter(f.col(datetime_field).cast('date') == day) \
        .groupBy(author_name_field, author_email_field,
                 repo_name_field, language_field,
                 license_field, company_field) \
        .agg(f.count(commits_id_field).alias(result_field))
