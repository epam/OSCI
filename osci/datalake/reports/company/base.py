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

from osci.datalake import DataLake, BaseReportFactory
from osci.datalake.reports import BaseReport

from typing import Type


class CompanyReport(BaseReport):
    def __init__(self, date: datetime, company: str):
        self.date = date
        self.company = company
        self.validate()

    def _check_company(self):
        if not self.company:
            raise ValueError('The field company cannot be empty')

    def validate(self):
        self._check_company()

    @property
    def full_name(self) -> str:
        return f'{self.company.upper()}_{self._get_name_with_date(self.date)}'

    @property
    def url(self) -> str:
        return DataLake().public.get_report_url(report_name=self.name, date=self.date, company=self.company)

    @property
    def path(self) -> str:
        return DataLake().public.get_report_path(report_name=self.name, date=self.date, company=self.company)

    def save(self, df: pd.DataFrame):
        DataLake().public.save_report(report_df=df, report_name=self.name, date=self.date, company=self.company)

    def read(self) -> pd.DataFrame:
        return DataLake().public.get_report(report_name=self.name, date=self.date, company=self.company)

    def read_all(self):
        return DataLake().public\
            .get_reports_for_last_days_of_month(report_name=self.name, date=self.date, company=self.company)


class CompanyReportFactory(BaseReportFactory):
    report_base_cls: Type[CompanyReport] = CompanyReport

    def get_cls(self, date_period: str) -> report_base_cls:
        return super(CompanyReportFactory, self).get_cls(date_period)

