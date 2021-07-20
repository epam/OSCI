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

from osci.datalake.reports.general.licensed_commits_ranking import OSCILicensesFactory
from osci.datalake.schemas.staging import PushEventsCommitsSchema
from osci.jobs.base import PushCommitsRankingJob
from osci.transformers.licenses import get_licenses_commits


class OSCILicensesJob(PushCommitsRankingJob):
    """Job that generates OSCI commits enriched with licenses"""
    REPORT_FACTORY = OSCILicensesFactory

    def transform(self, df: DataFrame, **kwargs) -> DataFrame:
        report_schema = self.report_cls.schema
        return get_licenses_commits(df=df,
                                    company=PushEventsCommitsSchema.company,
                                    license=PushEventsCommitsSchema.license,
                                    commits_id_field=PushEventsCommitsSchema.sha,
                                    result_field=report_schema.commits) \
            .withColumnRenamed(PushEventsCommitsSchema.company, report_schema.company) \
            .withColumnRenamed(PushEventsCommitsSchema.license, report_schema.license)
