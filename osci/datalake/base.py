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
from typing import Union, List, Iterable, Tuple, Iterator
from datetime import datetime
from pathlib import Path
from io import BytesIO

import abc
import re
import json
import pandas as pd

from .schemas import LandingSchemas, StagingSchemas, PublicSchemas
from osci.utils import normalize_company


class DatePeriodType:
    DTD = 'DTD'
    MTD = 'MTD'
    YTD = 'YTD'
    MBM = 'MBM'

    all = frozenset({DTD, MTD, YTD})


class BaseDataLakeArea(metaclass=abc.ABCMeta):
    """Base class for all data lake areas that should implement given interface."""

    def add_fs_prefix(self, path: Union[str, Path]) -> str:
        raise NotImplementedError()

    def get_spark_paths(self, paths: Iterable[Union[str, Path]]) -> List[str]:
        return [self.add_fs_prefix(path) for path in paths]

    @property
    def _github_events_commits_base(self):
        return 'github/events/push'

    @staticmethod
    def get_excel_writer() -> Tuple[pd.ExcelWriter, BytesIO]:
        buffer = BytesIO()
        return pd.ExcelWriter(buffer, engine='xlsxwriter'), buffer

    def write_bytes_to_file(self, path: Union[str, Path], buffer: BytesIO):
        raise NotImplementedError()


class BaseLandingArea(BaseDataLakeArea, abc.ABC):
    schemas = LandingSchemas

    @property
    def _github_repositories_base(self):
        return 'github/repository'

    def save_push_events_commits(self, push_event_commits, date: datetime):
        raise NotImplementedError()

    def get_hour_push_events_commits(self, date: datetime):
        raise NotImplementedError()

    def get_daily_push_events_commits(self, date: datetime):
        raise NotImplementedError()

    def save_repositories(self, df: pd.DataFrame, date: datetime):
        raise NotImplementedError()

    def get_repositories(self, date: datetime) -> pd.DataFrame:
        raise NotImplementedError()


class BaseStagingArea(BaseDataLakeArea, abc.ABC):
    CONF_AREA_DIR = 'configuration'
    schemas = StagingSchemas

    def get_push_events_commits(self, to_date: datetime, date_period_type: str = DatePeriodType.YTD,
                                from_date: datetime = None, company=None):
        raise NotImplementedError()

    def save_push_events_commits(self, push_event_commits: pd.DataFrame, company_name: str, date: datetime):
        raise NotImplementedError()

    def save_private_push_events_commits(self, push_event_commits: pd.DataFrame, company_name: str, date: datetime):
        raise NotImplementedError()

    def get_push_events_commits_spark_paths(self, to_date: datetime, date_period_type: str = DatePeriodType.YTD,
                                            from_date: datetime = None, company: str = None) -> List[str]:
        raise NotImplementedError()

    @staticmethod
    def _get_file_name(path) -> str:
        raise NotImplementedError()

    push_commits_filename_pattern = r'^(?P<company>(\d|\w|_)+)-(?P<date>\d{4}-\d{2}-\d{2}).parquet$'

    def filter_push_commit_file(self, file_name: str, to_date: datetime, from_date: datetime = None):
        match = re.match(self.push_commits_filename_pattern, file_name)
        if match:
            date = datetime.strptime(match.group('date'), '%Y-%m-%d')
            return date <= to_date and (from_date is None or date >= from_date)
        return None

    def get_push_events_commits_paths(self, to_date: datetime, date_period_type: str = DatePeriodType.YTD,
                                      from_date: datetime = None, company=None) -> Iterable[str]:
        year, month, day = None, None, None
        if date_period_type == DatePeriodType.DTD:
            if from_date is None:
                raise ValueError(f'`from_date` must be non None for {DatePeriodType.DTD} passed: {from_date}')
            if to_date < from_date:
                raise ValueError(f'`from_date` {from_date} must be less than `to_date` {to_date}')
            if to_date.year == from_date.year:
                year = to_date.year
                if to_date.month == from_date.month:
                    month = to_date.month
                    if to_date.day == from_date.day:
                        day = to_date.day
        elif date_period_type == DatePeriodType.MTD:
            year, month = to_date.year, to_date.month
        elif date_period_type == DatePeriodType.YTD:
            year = to_date.year
        else:
            raise ValueError(f'Unsupported date period type: {date_period_type} not in {DatePeriodType.all}')

        return filter(
            lambda path: self.filter_push_commit_file(self._get_file_name(path), from_date=from_date, to_date=to_date),
            self._get_date_partitioned_paths(dir_path=self._github_events_commits_base,
                                             year=year, month=month, day=day, company=company)
        )

    def _get_date_partitioned_paths(self, dir_path: str, year: Union[str, int] = None,
                                    month: Union[str, int] = None,
                                    day: Union[str, int] = None,
                                    company: str = None) -> Iterable[str]:
        raise NotImplementedError()

    def _get_configuration_file_path(self, path: str) -> str:
        raise NotImplementedError()

    def load_projects_filter(self):
        raise NotImplementedError()

    _repositories_file_format = 'parquet'

    def _get_repositories_file_name(self, date: datetime) -> str:
        return f'repository-{date:%Y-%m-%d}.{self._repositories_file_format}'

    def get_repositories_path(self, date: datetime) -> Union[Path, str]:
        raise NotImplementedError()

    def get_repositories_spark_path(self, date: datetime) -> Union[Path, str]:
        return self.add_fs_prefix(path=self.get_repositories_path(date=date))

    def get_repositories(self, date: datetime) -> pd.DataFrame:
        raise NotImplementedError()

    def save_repositories(self, df: pd.DataFrame, date: datetime):
        raise NotImplementedError()

    @staticmethod
    def _get_raw_push_events_commits_file_name(date: datetime, company: str) -> str:
        return f'{normalize_company(company)}-{date:%Y-%m-%d}.parquet'

    def get_raw_push_events_commits_path(self, date: datetime, company: str) -> Union[Path, str]:
        raise NotImplementedError()

    def get_raw_push_events_commits(self, path: Union[str, Path]) -> pd.DataFrame:
        raise NotImplementedError()

    def save_raw_push_events_commits(self, push_event_commits: pd.DataFrame, company_name: str, date: datetime):
        raise NotImplementedError()

    def get_daily_raw_push_events_commits_paths(self, date: datetime) -> Iterator[Union[str, Path]]:
        raise NotImplementedError()

    def get_daily_raw_push_events_commits(self, date: datetime) -> Iterator[Tuple[str, pd.DataFrame]]:
        for path in self.get_daily_raw_push_events_commits_paths(date=date):
            match = re.match(self.push_commits_filename_pattern, self._get_file_name(path))
            if match:
                company = match.group('company')
                df = self.get_raw_push_events_commits(path)
                if not df.empty:
                    yield company, df

    def get_union_daily_raw_push_events_commits(self, date: datetime) -> pd.DataFrame:
        result_df = pd.DataFrame()
        for path in self.get_daily_raw_push_events_commits_paths(date=date):
            df = self.get_raw_push_events_commits(path)
            if not df.empty:
                result_df = pd.concat([result_df, df])
        return result_df


class BasePublicArea(BaseDataLakeArea, abc.ABC):
    schemas = PublicSchemas

    def get_report_path(self, report_name: str, date: datetime, company: str = None) -> str:
        raise NotImplementedError()

    def save_report(self, report_df: pd.DataFrame, report_name: str, date: datetime, company: str = None):
        raise NotImplementedError()

    def get_report(self, report_name: str, date: datetime, company: str = None) -> pd.DataFrame:
        raise NotImplementedError()

    def get_report_url(self, report_name: str, date: datetime, company: str = None):
        raise NotImplementedError()

    def get_reports_for_last_days_of_month(self, report_name: str, date: datetime, company: str = None):
        raise NotImplementedError()

    def get_osci_change_excel_report_path(self, base_report_name: str, report_dir_name: str, date: datetime):
        raise NotImplementedError()

    def get_osci_change_excel_report_url(self, base_report_name: str, date: datetime, report_dir_name: str):
        raise NotImplementedError

    @staticmethod
    def get_osci_change_excel_report_name(base_report_name: str, date: datetime):
        return f'{date:%Y-%m-%d}_{base_report_name}.xlsx'

    def save_solutions_hub_osci_change_report_view(self, change_report: pd.DataFrame, report_dir_name: str,
                                                   old_date: datetime, new_date: datetime):
        writer, buffer = self.get_excel_writer()
        sheet_name = 'OSCI_Ranking'

        change_report.to_excel(writer, sheet_name=sheet_name, startrow=2, startcol=1)

        worksheet = writer.sheets[sheet_name]
        worksheet.write(0, 1, old_date.strftime('%Y (differences from %B, %d  ') + new_date.strftime('to %B, %d)'))
        worksheet.write(3, 9, '1 Active Contributors are those who authored 10 or more pushes in the time period')
        worksheet.write(4, 9, '2 Total Community counts those who authored 1 or more pushes in the time period')
        worksheet.write(5, 9, '* Changes are relative to the metrics at the end of the previous month')
        worksheet.write(6, 9, 'The top 100 is calculated using the Active Contributors metric')
        worksheet.write(7, 9, 'If two companies have equal Active Contributors, '
                              'their relative positions are determined by Total Community')
        writer.save()

        self.write_bytes_to_file(path=self.get_osci_change_excel_report_path(base_report_name=sheet_name,
                                                                             report_dir_name=report_dir_name,
                                                                             date=new_date),
                                 buffer=buffer)

    def save_email(self, email_body: str, date: datetime):
        raise NotImplementedError()

    def get_companies_contributors_repository_commits_path(self, date: datetime) -> Union[str, Path]:
        raise NotImplementedError()

    def get_companies_contributors_repository_commits_spark_path(self, date) -> str:
        return self.add_fs_prefix(path=self.get_companies_contributors_repository_commits_path(date=date))

    def save_companies_contributors_repository_commits(self, df: pd.DataFrame, date: datetime):
        raise NotImplementedError()

    def get_companies_contributors_repository_commits(self, date: datetime) -> pd.DataFrame:
        raise NotImplementedError()


class BaseWebArea(abc.ABC):

    _osci_ranking_dir_name = 'osci-ranking'
    _osci_ranking_monthly_dir_name = 'monthly'

    def _join_paths(self, *paths: Union[str, Path], create_if_not_exists=False) -> Union[str, Path]:
        raise NotImplementedError()

    def _save_json(self, path: Union[str, Path], json_data: str):
        raise NotImplementedError()

    @property
    def osci_ranking_dir(self) -> Union[str, Path]:
        raise NotImplementedError()

    def generate_monthly_osci_ranking_dir_path(self, date: datetime) -> Union[str, Path]:
        return self._join_paths(
            self.osci_ranking_dir,
            self._osci_ranking_monthly_dir_name,
            f'{date:%Y}',
            create_if_not_exists=True
        )

    def get_osci_ranking_monthly_path(self, date: datetime) -> Union[str, Path]:
        return self._join_paths(
            self.generate_monthly_osci_ranking_dir_path(date=date),
            f'{date:%m}.json'
        )

    def save(self, path: Union[str, Path], data):
        self._save_json(
            path=path,
            json_data=json.dumps(data, default=lambda v: f'{v:%Y-%m-%d}' if isinstance(v, datetime) else str(v))
        )

    def save_monthly_osci_ranking(self, ranking: dict, date: datetime):
        self.save(
            path=self.get_osci_ranking_monthly_path(date=date),
            data=ranking
        )
