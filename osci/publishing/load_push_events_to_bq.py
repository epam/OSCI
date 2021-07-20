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
from osci.datalake import DataLake, DatePeriodType
from osci.datalake.schemas.bq import BigQueryPushEventsCommitsColumns
from typing import Dict, Any


def load_push_events_to_bq(date: datetime.datetime, hour: int) -> Dict[str, Dict[str, Any]]:
    date = date.replace(hour=hour)
    df = DataLake().staging.get_push_events_commits(from_date=date,
                                                    to_date=date,
                                                    date_period_type=DatePeriodType.DTD)
    job_results = DataLake().big_query.load_dataframe(df=df, table_id=BigQueryPushEventsCommitsColumns.table_id,
                                                      schema=BigQueryPushEventsCommitsColumns.schema)
    return {'num_rows': job_results.num_rows,
            'num_columns': len(job_results.schema),
            'table_id': BigQueryPushEventsCommitsColumns.table_id}
