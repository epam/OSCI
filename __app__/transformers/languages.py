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


def get_languages_commits(df: DataFrame, company: str, language: str, commits_id_field: str,
                          result_field: str = 'Commits') -> DataFrame:
    """Get commits that are enriched with languages

    :param df: PushEventsCommits
    :param company: Company name field
    :param language: language in commits
    :param commits_id_field: Commit identifier (such as SHA)
    :param result_field: Field in output df which must contains amount of commits
    :return:
    """
    return df.select(f.col(company), f.col(language), f.col(commits_id_field)) \
        .where(f.col(language).isNotNull()) \
        .groupby(company, language) \
        .agg(f.count(commits_id_field).alias(result_field))
