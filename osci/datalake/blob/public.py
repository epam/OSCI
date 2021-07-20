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
from calendar import monthrange
from typing import List, Tuple

from .base import BlobArea
from osci.datalake.base import BasePublicArea
from osci.utils import normalize_company

import logging
import pandas as pd
import re

log = logging.getLogger(__name__)


class BlobPublicArea(BasePublicArea, BlobArea):
    AREA_CONTAINER = 'public'

    @property
    def _report_base_path(self) -> str:
        return 'report'

    def get_report_path(self, report_name: str, date: datetime, company: str = None) -> str:
        path = self._report_base_path
        if company is not None:
            company = normalize_company(name=company)
            path = f'{path}/{company}'
        return date.strftime(f'{path}/{report_name}/{company.upper() + "_" if company else ""}{report_name}_%Y-%m-%d.csv')

    def get_report_url(self, report_name: str, date: datetime, company: str = None):
        report_path = self.get_report_path(report_name=report_name, date=date, company=company)
        return self.add_http_prefix(report_path)

    def get_osci_change_excel_report_url(self, base_report_name: str, date: datetime, report_dir_name: str):
        return self.add_http_prefix(self.get_osci_change_excel_report_path(base_report_name=base_report_name,
                                                                           date=date,
                                                                           report_dir_name=report_dir_name))

    def save_report(self, report_df: pd.DataFrame, report_name: str, date: datetime, company: str = None):
        """Save report dataframe to csv

        :param report_df: report dataframe
        :param report_name: report name
        :param date: date of report
        :param company: company name
        """
        self.write_pandas_dataframe_to_csv(df=report_df,
                                           path=self.get_report_path(report_name=report_name,
                                                                     date=date,
                                                                     company=company))

    def get_report(self, report_name: str, date: datetime, company: str = None) -> pd.DataFrame:
        return self.read_pandas_dataframe_from_csv(path=self.get_report_path(report_name=report_name,
                                                                             date=date,
                                                                             company=company))

    def get_osci_change_excel_report_path(self, base_report_name: str, report_dir_name: str, date: datetime):
        return f"{self._report_base_path}/" \
               f"{report_dir_name}/" \
               f"{self.get_osci_change_excel_report_name(base_report_name, date)}"

    def get_reports_for_last_days_of_month(self, report_name: str, date: datetime, company: str = None) -> List[Tuple[datetime, pd.DataFrame]]:
        path = self._report_base_path
        if company is not None:
            company = normalize_company(name=company)
            path = f'{path}/{company}'
        path = date.strftime(f'{path}/{report_name}/{company.upper() + "_" if company else ""}{report_name}_%Y')

        reports_set = []
        for report in self.container_client.list_blobs(name_starts_with=path):
            report_name = report['name']
            match = re.search(pattern=r'\d{4}-\d{2}-\d{2}', string=report_name)
            report_date = datetime.strptime(match.group(), '%Y-%m-%d').date()
            date = datetime(year=report_date.year,
                            month=report_date.month,
                            day=monthrange(report_date.year, report_date.month)[1])
            if report_date.strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d'):
                reports_set.append((report_date, self.read_pandas_dataframe_from_csv(path=report_name)))
        return reports_set

    @property
    def _email_base_path(self) -> str:
        return 'email'

    def _get_email_path(self, date: datetime) -> str:
        return date.strftime(f"{self._email_base_path}/%Y-%m-%d.html")

    def save_email(self, email_body: str, date: datetime):
        self.write_string_to_file(path=self._get_email_path(date=date), data=email_body, content_type='text/html')
