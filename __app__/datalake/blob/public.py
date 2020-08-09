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

from .base import BlobArea
from __app__.datalake.base import BasePublicArea
from __app__.utils import normalize_company

import logging
import pandas as pd

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

    def _get_osci_change_report_path(self, report_name: str, report_dir_name: str,  date: datetime):
        return date.strftime(f"{self._report_base_path}/{report_dir_name}/%Y-%m-%d_{report_name}.xlsx")

