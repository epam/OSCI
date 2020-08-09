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


import datetime
import logging
import azure.functions as func
import traceback as tb

from __app__.datalake import DataLake
from __app__.datalake.schemas.bq import BigQueryPushEventsCommitsColumns
from __app__.datalake.schemas.staging import PushEventsCommitsSchema
from __app__.utils import get_req_param

DAY_FORMAT = "%Y-%m-%d"
DEFAULT_DAY = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(DAY_FORMAT)

log = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        log.info(f"Http trigger. req.params: {req.params}")
        date = datetime.datetime.strptime(get_req_param(req, 'date', default=DEFAULT_DAY), DAY_FORMAT)
        for blob_path in DataLake().staging.get_push_events_commits_paths(to_date=date):
            df = DataLake().staging.get_push_events_commits(blob_path)[PushEventsCommitsSchema.required]
            job_results = DataLake().big_query.load_dataframe(df=df,
                                                              table_id=BigQueryPushEventsCommitsColumns.table_id,
                                                              schema=BigQueryPushEventsCommitsColumns.schema)
            logging.info("{} rows and {} columns in {}".format(job_results.num_rows,
                                                               len(job_results.schema),
                                                               BigQueryPushEventsCommitsColumns.table_id))
    except Exception as ex:
        log.error(f'Exception {ex}')
        log.exception(ex)
        return func.HttpResponse(f"This HTTP triggered function failed {ex} "
                                 f"{''.join(tb.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))}",
                                 status_code=500)
    finally:
        return func.HttpResponse(f"This HTTP triggered function executed")
