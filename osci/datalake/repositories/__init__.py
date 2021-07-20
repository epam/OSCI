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
from osci.datalake import DataLake

import datetime
import pandas as pd


class Repositories:
    schema = DataLake().staging.schemas.repositories

    def __init__(self, date: datetime.datetime):
        self.date = date

    @property
    def path(self) -> str:
        """
        Return the full path to repositories
        """
        return DataLake().staging.get_repositories_path(self.date)

    @property
    def spark_path(self) -> str:
        """
        Return the full path to repositories
        """
        return DataLake().staging.get_repositories_spark_path(self.date)

    def save(self, df: pd.DataFrame):
        """
        Save pandas DataFrame as file
        :param df:
        """
        return DataLake().staging.save_repositories(df, self.date)

    def read(self) -> pd.DataFrame:
        """
        Read repositories to pandas DataFrame from file
        """
        return DataLake().staging.get_repositories(self.date)
