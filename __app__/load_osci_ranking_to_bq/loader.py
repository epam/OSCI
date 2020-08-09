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
from __app__.datalake import DataLake
from __app__.datalake.schemas.bq import BigQueryOSCIRankingReport
from __app__.datalake.schemas.public import PublicSchemas

import datetime
import logging

log = logging.getLogger(__name__)


def load_osci_ranking_to_bq(date: datetime.datetime):
    report = DataLake().public.get_report(report_name='OSCI_ranking_YTD', date=date)
    report = report[PublicSchemas.company_contributors_ranking.required]
    report = report.reset_index().rename(columns={'index': BigQueryOSCIRankingReport.Columns.position})
    report = report.rename(columns=BigQueryOSCIRankingReport.mapping)
    report[BigQueryOSCIRankingReport.Columns.date] = date.date()

    return DataLake().big_query.load_dataframe(df=report, table_id=BigQueryOSCIRankingReport.table_id,
                                               schema=BigQueryOSCIRankingReport.schema)
