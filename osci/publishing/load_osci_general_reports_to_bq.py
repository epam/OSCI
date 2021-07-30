"""Copyright since 2021, EPAM Systems

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

from osci.datalake import DataLake
from osci.datalake.reports.general import OSCIGeneralRanking
from osci.datalake.schemas.bq import BigQueryOSCIGeneralRankingReport
from osci.datalake.schemas.public import PublicSchemas

import logging

log = logging.getLogger(__name__)


def load_osci_general_reports_to_bq(date: datetime.datetime):
    report = OSCIGeneralRanking(date=date)
    table = BigQueryOSCIGeneralRankingReport
    log.debug(f'Load {report.name} for {date:%Y-%m-%d} to {table.table_id}')
    report_df = report.read()
    report_df = report_df[PublicSchemas.osci_general_report.required]
    report_df[table.Columns.position] += 1
    report_df = report_df.rename(columns=table.mapping)
    report_df[table.Columns.date] = date
    return DataLake().big_query.load_dataframe(df=report_df, table_id=table.table_id, schema=table.schema)
