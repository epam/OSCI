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
from __app__.utils import get_req_param
from __app__.datalake import DatePeriodType
from .loader import load_osci_ranking_to_bq

import datetime
import logging
import traceback as tb
import azure.functions as func
import json

DAY_FORMAT = "%Y-%m-%d"
DEFAULT_DAY = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(DAY_FORMAT)
log = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
    try:
        log.info(f"Http trigger. req.params: {req.params}")

        date = datetime.datetime.strptime(get_req_param(req, 'date', default=DEFAULT_DAY), DAY_FORMAT)
        date_period = get_req_param(req, 'date_period', default=DatePeriodType.YTD)
        table = load_osci_ranking_to_bq(date=date, date_period=date_period)
        return func.HttpResponse(json.dumps({'table': {'id': table.table_id, 'rows': table.num_rows}}))
    except Exception as ex:
        log.error(f'Exception {ex}')
        log.exception(ex)
        return func.HttpResponse(f"This HTTP triggered function failed {ex} "
                                 f"{''.join(tb.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))}",
                                 status_code=500)
