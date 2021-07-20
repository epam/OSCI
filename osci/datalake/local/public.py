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
from glob import glob
from pathlib import Path
from typing import List, Tuple

from .base import LocalSystemArea
from osci.datalake.base import BasePublicArea
from osci.utils import normalize_company

import re
import logging
import pandas as pd

log = logging.getLogger(__name__)


class LocalPublicArea(BasePublicArea, LocalSystemArea):
    BASE_AREA_DIR = 'public'

    @property
    def _report_base_path(self) -> Path:
        return self.BASE_PATH / self.BASE_AREA_DIR / 'report'

    def get_report_path(self, report_name: str, date: datetime, company: str = None) -> Path:
        path = self._report_base_path
        if company is not None:
            company = normalize_company(name=company)
            path /= company
        path = path / report_name
        path.mkdir(parents=True, exist_ok=True)
        filename = f'{company.upper() + "_" if company else ""}{report_name}_{date.strftime("%Y-%m-%d")}.csv'
        return path / filename

    def get_report_url(self, report_name: str, date: datetime, company: str = None):
        report_path = self.get_report_path(report_name=report_name, date=date, company=company)
        return self.add_fs_absolute_prefix(path=report_path)

    def get_osci_change_excel_report_url(self, base_report_name: str, date: datetime, report_dir_name: str):
        return self.add_fs_absolute_prefix(self.get_osci_change_excel_report_path(base_report_name=base_report_name,
                                                                                  report_dir_name=report_dir_name,
                                                                                  date=date))

    def get_reports_for_last_days_of_month(self, report_name: str, date: datetime, company: str = None) -> List[Tuple[datetime, pd.DataFrame]]:
        path = self._report_base_path
        if company is not None:
            company = normalize_company(name=company)
            path = f'{path}/{company}'
        path = date.strftime(f'{path}/{report_name}/{company.upper() + "_" if company else ""}{report_name}_%Y*')

        reports_set = []
        for report_name in glob(path):
            match = re.search(pattern=r'\d{4}-\d{2}-\d{2}', string=report_name)
            report_date = datetime.strptime(match.group(), '%Y-%m-%d').date()
            date = datetime(year=report_date.year,
                            month=report_date.month,
                            day=monthrange(report_date.year, report_date.month)[1])
            if report_date.strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d'):
                reports_set.append((report_date, pd.read_csv(report_name)))
        return reports_set

    def save_report(self, report_df: pd.DataFrame, report_name: str, date: datetime, company: str = None):
        path = self.get_report_path(report_name, date, company)
        report_df.to_csv(path, index=False)

    def get_report(self, report_name: str, date: datetime, company: str = None) -> pd.DataFrame:
        path = self.get_report_path(report_name, date, company)
        return pd.read_csv(path)

    def get_osci_change_excel_report_path(self, base_report_name: str, report_dir_name: str, date: datetime):
        path = self._report_base_path
        path = path / report_dir_name
        path.mkdir(parents=True, exist_ok=True)
        filename = self.get_osci_change_excel_report_name(base_report_name, date)
        return path / filename

    @property
    def _email_base_path(self) -> Path:
        return self.BASE_PATH / self.BASE_AREA_DIR / 'email'

    def _get_email_path(self, date: datetime) -> Path:
        path = self._email_base_path
        path.mkdir(parents=True, exist_ok=True)
        return path / date.strftime(f"%Y-%m-%d.html")

    def save_email(self, email_body: str, date: datetime):
        with open(str(self._get_email_path(date=date)), 'w', encoding='utf-8') as f:
            f.write(email_body)
