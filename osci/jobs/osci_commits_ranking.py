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
from osci.transformers.rankers.commits_ranking import get_commits_ranking
from osci.datalake.reports.general.commits_ranking import OSCICommitsRankingFactory
from .base import PushCommitsRankingJob


class OSCICommitsRankingJob(PushCommitsRankingJob):
    """Job that generates OSCI commits ranking report"""
    REPORT_FACTORY = OSCICommitsRankingFactory

    def transform(self, df: DataFrame, **kwargs) -> DataFrame:
        report_schema = self.report_cls.schema
        return get_commits_ranking(df=df,
                                   commits_id_field=self.commits_schema.sha,
                                   company_field=self.commits_schema.company,
                                   result_field=report_schema.commits) \
            .withColumnRenamed(self.commits_schema.company, report_schema.company)
