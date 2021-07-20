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
from osci.transformers.rankers.employees_ranking import (get_companies_employees_activity_rank_combined,
                                                            CommitsThresholds)
from osci.datalake.reports.general.osci_ranking import OSCIRankingFactory
from .base import PushCommitsRankingJob


class OSCIRankingJob(PushCommitsRankingJob):
    REPORT_FACTORY = OSCIRankingFactory

    def transform(self, df: DataFrame, **kwargs) -> DataFrame:
        report_schema = self.report_cls.schema
        thresholds = [
            CommitsThresholds(col=report_schema.total, threshold=1),
            CommitsThresholds(col=report_schema.active, threshold=10)
        ]
        return get_companies_employees_activity_rank_combined(df=df,
                                                              commits_id_field=self.commits_schema.sha,
                                                              author_email_field=self.commits_schema.author_email,
                                                              company_field=self.commits_schema.company,
                                                              commits_thresholds=thresholds,
                                                              order_by_field=report_schema.active
                                                              ) \
            .withColumnRenamed(self.commits_schema.company, report_schema.company)
