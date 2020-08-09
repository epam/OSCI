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

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as f


def filter_out_duplicates(df: DataFrame, commits_id_field: str, datetime_field: str) -> DataFrame:
    window = Window.partitionBy(f.col(commits_id_field)).orderBy((f.col(datetime_field)))
    return df \
        .select(f.col('*'), f.row_number().over(window).alias('row_number')) \
        .where(f.col('row_number') == 1).drop(f.col('row_number'))
