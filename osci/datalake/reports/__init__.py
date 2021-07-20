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
import abc
import datetime

import pandas as pd

from typing import Type, Dict

from osci.utils import MetaSingleton


class BaseReport(metaclass=abc.ABCMeta):
    base_name = None
    date_period = None
    schema = None

    __date_suffix_pattern = "%Y-%m-%d"

    __data = None

    @property
    def name(self) -> str:
        """
        Return the base_name of the report with date period type
        """
        return f'{self.base_name}{"_" + self.date_period if self.date_period else ""}'

    def _get_name_with_date(self, date: datetime) -> str:
        """
        Return the name of the report with date
        :param date:
        :return:
        """
        return f'{self.name}_{date.strftime(self.__date_suffix_pattern)}.csv'

    @property
    def full_name(self) -> str:
        """
        Return the full name of the report including file extension
        """
        raise NotImplementedError()

    @property
    def url(self) -> str:
        """
        Return the report url with prefix
        """
        raise NotImplementedError()

    @property
    def path(self) -> str:
        """
        Return the full path to report
        """
        raise NotImplementedError()

    @property
    def df(self) -> pd.DataFrame:
        """
        Return report data as pandas DataFrame
        """
        if self.__data is None:
            self.__data = self.read()
        return self.__data

    def save(self, df: pd.DataFrame):
        """
        Save pandas DataFrame as file
        :param df:
        """
        raise NotImplementedError()

    def read(self) -> pd.DataFrame:
        """
        Read report to pandas DataFrame from file
        """
        raise NotImplementedError()


class BaseReportFactory(metaclass=MetaSingleton):
    report_base_cls: Type[BaseReport] = BaseReport
    __date_period_cls_map__: Dict[str, report_base_cls] = None

    def __create_period_cls_map(self) -> Dict[str, report_base_cls]:
        return {
            cls.date_period: cls
            for cls in self.report_base_cls.__subclasses__()
        }

    @property
    def _date_period_cls_map(self) -> Dict[str, report_base_cls]:
        if self.__date_period_cls_map__ is None:
            self.__date_period_cls_map__ = self.__create_period_cls_map()
        return self.__date_period_cls_map__

    def get_cls(self, date_period: str) -> report_base_cls:
        if date_period not in self._date_period_cls_map:
            raise NotImplementedError(f'Subclass of {self.report_base_cls} not implemented for '
                                      f'date period `{date_period}`')
        return self._date_period_cls_map[date_period]
