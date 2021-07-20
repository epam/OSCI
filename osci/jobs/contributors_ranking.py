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
from osci.transformers.rankers.commits_ranking import get_employees_commits_amount
from osci.datalake.reports.company.contributors import ContributorsRankingFactory
from .base import CompanyPushCommitsRankingJob


class ContributorsRankingJob(CompanyPushCommitsRankingJob):
    REPORT_FACTORY = ContributorsRankingFactory

    def transform(self, df: DataFrame, **kwargs) -> DataFrame:
        report_schema = self.report_cls.schema
        return get_employees_commits_amount(df=df,
                                            author_email_field=self.commits_schema.author_email,
                                            author_name_field=self.commits_schema.author_name,
                                            commits_id_field=self.commits_schema.sha,
                                            result_field=report_schema.commits) \
            .withColumnRenamed(self.commits_schema.author_name, report_schema.author) \
            .withColumnRenamed(self.commits_schema.author_email, report_schema.author_email)
