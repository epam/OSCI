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
from osci.datalake.reports.general.language_commits_ranking import OSCILanguagesFactory
from osci.datalake.schemas.staging import PushEventsCommitsSchema
from osci.transformers.languages import get_languages_commits
from .base import PushCommitsRankingJob

from pyspark.sql import DataFrame


class OSCILanguagesJob(PushCommitsRankingJob):
    """Job that generates OSCI commits enriched with programming languages"""
    REPORT_FACTORY = OSCILanguagesFactory

    def transform(self, df: DataFrame, **kwargs) -> DataFrame:
        report_schema = self.report_cls.schema
        return get_languages_commits(df=df,
                                     company=PushEventsCommitsSchema.company,
                                     language=PushEventsCommitsSchema.language,
                                     commits_id_field=PushEventsCommitsSchema.sha,
                                     result_field=report_schema.commits) \
            .withColumnRenamed(PushEventsCommitsSchema.company, report_schema.company) \
            .withColumnRenamed(PushEventsCommitsSchema.language, report_schema.language)
