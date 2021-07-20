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

import datetime

import pandas as pd

from osci.datalake import DataLake
from osci.datalake.reports import BaseReport, BaseReportFactory

from typing import Type


class Report(BaseReport):
    def __init__(self, date: datetime):
        self.date = date

    @property
    def full_name(self) -> str:
        return self._get_name_with_date(self.date)

    @property
    def url(self) -> str:
        return DataLake().public.get_report_url(report_name=self.name, date=self.date)

    @property
    def path(self) -> str:
        return DataLake().public.get_report_path(report_name=self.name, date=self.date)

    def save(self, df: pd.DataFrame):
        DataLake().public.save_report(report_df=df, report_name=self.name, date=self.date)

    def read(self) -> pd.DataFrame:
        return DataLake().public.get_report(report_name=self.name, date=self.date)


class GeneralReportFactory(BaseReportFactory):
    report_base_cls: Type[Report] = Report

    def get_cls(self, date_period: str) -> report_base_cls:
        return super(GeneralReportFactory, self).get_cls(date_period)
