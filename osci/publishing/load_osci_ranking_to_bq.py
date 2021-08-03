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
from osci.datalake import DataLake, DatePeriodType
from osci.datalake.reports.general.osci_ranking import OSCIRankingFactory
from osci.datalake.schemas.bq import (BigQueryOSCIRankingReport,
                                         BigQueryOSCIRankingReportMTD,
                                         BaseBigQueryOSCIRankingReport)
from osci.datalake.schemas.public import PublicSchemas

from typing import Dict

import datetime
import logging

log = logging.getLogger(__name__)

date_period_to_table_map: Dict[str, BaseBigQueryOSCIRankingReport.__class__] = {
    DatePeriodType.YTD: BigQueryOSCIRankingReport,
    DatePeriodType.MTD: BigQueryOSCIRankingReportMTD,
}


def load_osci_ranking_to_bq(date: datetime.datetime, date_period: str = DatePeriodType.YTD):
    if date_period not in (DatePeriodType.MTD, DatePeriodType.YTD):
        raise ValueError(f'Unsupported {date_period}')
    report = OSCIRankingFactory().get_cls(date_period=date_period)(date=date)
    table = date_period_to_table_map[date_period]

    log.debug(f'Load {report.name} for {date:%Y-%m-%d} to {table.table_id}')

    report_df = report.read()
    report_df = report_df[PublicSchemas.company_contributors_ranking.required]
    report_df = report_df.reset_index().rename(columns={'index': table.Columns.position})
    report_df[table.Columns.position] += 1
    report_df = report_df.rename(columns=table.mapping)
    report_df[table.Columns.date] = date.date()

    return DataLake().big_query.load_dataframe(df=report_df, table_id=table.table_id, schema=table.schema)
