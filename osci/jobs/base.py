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
import logging

from datetime import datetime
from pyspark.sql import DataFrame, functions as f
from typing import Type

from osci.datalake import DataLake, DatePeriodType, GeneralReportFactory, Report, CompanyReportFactory, CompanyReport
from osci.transformers.filter_duplicates import filter_out_duplicates
from .session import Session

log = logging.getLogger(__name__)


class PushCommitsRankingJob:
    """Base push commits ranking spark job"""
    REPORT_NAME = 'unnamed_report'
    REPORT_FACTORY: Type[GeneralReportFactory] = None
    report_cls: Type[Report]

    def __init__(self, date_period_type: str = DatePeriodType.YTD):
        self.data_lake = DataLake()
        self.commits_schema = self.data_lake.staging.schemas.push_commits
        self.date_period_type = date_period_type
        self.report_cls: Type[Report] = self.REPORT_FACTORY().get_cls(date_period=self.date_period_type)

    def extract(self, to_date: datetime, from_date: datetime = None) -> DataFrame:
        return self.filter_df(
            commits=Session().load_dataframe(paths=self._get_dataset_paths(to_date, from_date))
        )

    def _get_dataset_paths(self, to_date: datetime, from_date: datetime = None):
        paths = self.data_lake.staging.get_push_events_commits_spark_paths(from_date=from_date,
                                                                           to_date=to_date,
                                                                           date_period_type=self.date_period_type)
        log.debug(f'Loaded paths for ({from_date} {to_date}) {paths}')
        return paths

    def transform(self, df: DataFrame, *args, **kwargs) -> DataFrame:
        raise NotImplementedError()

    def load(self, df: DataFrame, date: datetime):
        self.report_cls(date=date).save(df=df.toPandas())

    def run(self, to_date: datetime, from_date: datetime = None):
        df = self.extract(to_date, from_date)
        df = self.transform(df)
        self.load(df, to_date)

    def filter_out_duplicates_commits(self, df) -> DataFrame:
        return filter_out_duplicates(df, commits_id_field=self.commits_schema.sha,
                                     datetime_field=self.commits_schema.event_created_at)

    def filter_out_na_org(self, df) -> DataFrame:
        return df.where(f.col(self.commits_schema.org_name).isNotNull())

    def filter_df(self, commits) -> DataFrame:
        return self.filter_out_duplicates_commits(commits)


class CompanyPushCommitsRankingJob(PushCommitsRankingJob):
    REPORT_FACTORY: CompanyReportFactory
    report_cls: Type[CompanyReport]

    def __init__(self, company: str, date_period_type: str = DatePeriodType.YTD):
        self.company = company
        super().__init__(date_period_type=date_period_type)

    def transform(self, df: DataFrame, *args, **kwargs) -> DataFrame:
        raise NotImplementedError()

    def _get_dataset_paths(self, to_date: datetime, from_date: datetime = None):
        return self.data_lake.staging.get_push_events_commits_spark_paths(from_date=from_date,
                                                                          to_date=to_date,
                                                                          date_period_type=self.date_period_type,
                                                                          company=self.company)

    def load(self, df: DataFrame, date: datetime):
        self.report_cls(date=date, company=self.company).save(df=df.toPandas())
