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
from datetime import datetime
from pyspark.sql import DataFrame, functions as f

from __app__.datalake import DataLake, DatePeriodType
from __app__.transformers.filter_duplicates import filter_out_duplicates
from .session import Session


class PushCommitsRankingJob:
    """Base push commits ranking spark job"""
    REPORT_NAME = 'unnamed_report'

    def __init__(self, company: str = None, date_period_type: str = DatePeriodType.YTD):
        self.data_lake = DataLake()
        self.commits_schema = self.data_lake.staging.schemas.push_commits
        self.company = company
        self.date_period_type = date_period_type

    def extract(self, to_date: datetime, from_date: datetime = None) -> DataFrame:
        return self.filter_df(
            df=Session().load_dataframe(
                paths=self.data_lake.staging.get_push_events_commits_spark_paths(from_date=from_date,
                                                                                 to_date=to_date,
                                                                                 date_period_type=self.date_period_type,
                                                                                 company=self.company)
            )
        )

    def transform(self, df: DataFrame, *args, **kwargs) -> DataFrame:
        raise NotImplementedError()

    def load(self, df: DataFrame, date: datetime):
        self.data_lake.public.save_report(report_df=df.toPandas(),
                                          report_name=self.report_name,
                                          date=date,
                                          company=self.company)

    def run(self, to_date: datetime, from_date: datetime = None):
        df = self.extract(to_date, from_date)
        df = self.transform(df)
        self.load(df, to_date)

    @property
    def report_name(self):
        return self.REPORT_NAME + (f'_{self.date_period_type}' if self.date_period_type != DatePeriodType.DTD else '')

    def filter_out_duplicates_commits(self, df) -> DataFrame:
        return filter_out_duplicates(df, commits_id_field=self.commits_schema.sha,
                                     datetime_field=self.commits_schema.event_created_at)

    def filter_out_na_org(self, df) -> DataFrame:
        return df.where(f.col(self.commits_schema.org_name).isNotNull())

    def filter_df(self, df) -> DataFrame:
        return self.filter_out_duplicates_commits(self.filter_out_na_org(df))
