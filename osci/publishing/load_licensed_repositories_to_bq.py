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
from osci.datalake.schemas.bq import BigQueryLicensedRepository
from google.cloud import bigquery

import datetime
import logging

log = logging.getLogger(__name__)


def load_licensed_repositories_to_bq(date: datetime.datetime) -> bigquery.table.Table:
    """Load licensed repositories to BigQuery for a given day"""
    df = DataLake().staging.get_repositories(date)
    return DataLake().big_query.load_dataframe(df=df,
                                               table_id=BigQueryLicensedRepository.table_id,
                                               schema=BigQueryLicensedRepository.schema)
