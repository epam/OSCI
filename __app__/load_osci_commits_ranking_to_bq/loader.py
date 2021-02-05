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
from __app__.datalake import DataLake, DatePeriodType
from __app__.datalake.schemas.bq import (BigQueryOSCICommitsRankingReport,
                                         BigQueryOSCICommitsRankingReportMTD,
                                         BaseBigQueryOSCICommitsRankingReport)
from __app__.datalake.schemas.public import PublicSchemas
from __app__.datalake.reports.general.commits_ranking import OSCICommitsRankingFactory

from typing import Dict

import datetime
import logging

log = logging.getLogger(__name__)

date_period_to_table_map: Dict[str, BaseBigQueryOSCICommitsRankingReport.__class__] = {
    DatePeriodType.YTD: BigQueryOSCICommitsRankingReport,
    DatePeriodType.MTD: BigQueryOSCICommitsRankingReportMTD,
}


def load_osci_commits_ranking_to_bq(date: datetime.datetime, date_period: str = DatePeriodType.YTD):
    if date_period not in (DatePeriodType.MTD, DatePeriodType.YTD):
        raise ValueError(f'Unsupported {date_period}')
    report = OSCICommitsRankingFactory().get_cls(date_period=date_period)(date=date)
    table = date_period_to_table_map[date_period]

    log.debug(date.strftime(f'Load {report.name} for %Y-%m-%d to {table.table_id}'))

    report_df = report.read()
    report_df = report_df[PublicSchemas.company_commits_ranking.required]
    report_df = report_df.reset_index().rename(columns={'index': table.Columns.position})
    report_df[table.Columns.position] += 1
    report_df = report_df.rename(columns=table.mapping)
    report_df[table.Columns.date] = date.date()

    return DataLake().big_query.load_dataframe(df=report_df, table_id=table.table_id, schema=table.schema)
