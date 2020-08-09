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
from __app__.transformers.rankers.commits_ranking import get_month_by_month_commits_amounts
from .base import PushCommitsRankingJob


class MonthByMonthCommitsJob(PushCommitsRankingJob):
    """Job that generates month-by-month amount of commits report"""
    REPORT_NAME = 'month_by_month_commits'

    def transform(self, df: DataFrame, **kwargs) -> DataFrame:
        report_schema = self.data_lake.public.schemas.month_by_month_commits
        return get_month_by_month_commits_amounts(df=df,
                                                  commits_id_field=self.commits_schema.sha,
                                                  datetime_field=self.commits_schema.event_created_at,
                                                  result_month_field=report_schema.month,
                                                  result_field=report_schema.commits_amount)
