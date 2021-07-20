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

from osci.transformers.contributors import get_osci_contributors
from osci.datalake.reports.general.osci_contributors_ranking import OSCIContributorsRankingFactory
from osci.datalake.schemas.public import OSCIContributorsRankingSchema
from osci.datalake.schemas.staging import PushEventsCommitsSchema as CommitsSchema

from .base import PushCommitsRankingJob


class OSCIContributorsRankingJob(PushCommitsRankingJob):
    """Job that generates OSCI contributors ranking"""
    REPORT_FACTORY = OSCIContributorsRankingFactory

    def transform(self, df: DataFrame, **kwargs) -> DataFrame:
        schema: OSCIContributorsRankingSchema = self.report_cls.schema
        return get_osci_contributors(df=df,
                                     author_name_field=CommitsSchema.author_name,
                                     author_email_field=CommitsSchema.author_email,
                                     company_field=CommitsSchema.company,
                                     commits_id_field=CommitsSchema.sha,
                                     result_field=schema.commits) \
            .withColumnRenamed(CommitsSchema.company, schema.company) \
            .withColumnRenamed(CommitsSchema.author_name, schema.author) \
            .withColumnRenamed(CommitsSchema.author_email, schema.author_email)
