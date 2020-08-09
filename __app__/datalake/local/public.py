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
from pathlib import Path

from .base import LocalSystemArea
from __app__.datalake.base import BasePublicArea
from __app__.utils import normalize_company

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

    def save_report(self, report_df: pd.DataFrame, report_name: str, date: datetime, company: str = None):
        path = self.get_report_path(report_name, date, company)
        report_df.to_csv(path, index=False)

    def get_report(self, report_name: str, date: datetime, company: str = None) -> pd.DataFrame:
        path = self.get_report_path(report_name, date, company)
        return pd.read_csv(path)

    def _get_osci_change_report_path(self, report_name: str, report_dir_name: str,  date: datetime):
        path = self._report_base_path
        path = path / report_dir_name
        path.mkdir(parents=True, exist_ok=True)
        filename = date.strftime(f"%Y-%m-%d_{report_name}.xlsx")
        return path / filename
