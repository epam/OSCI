"""Copyright since 2019, EPAM Systems

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
from .process import process_github_daily_push_events
from __app__.utils import get_req_param

import datetime
import logging
import azure.functions as func
import traceback as tb

DAY_FORMAT = "%Y-%m-%d"
DEFAULT_DAY = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(DAY_FORMAT)
log = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
    status_code = 200
    try:
        log.info(f"Http trigger. req.params: {req.params}")
        day = datetime.datetime.strptime(
            get_req_param(req, 'date', default=DEFAULT_DAY),
            DAY_FORMAT
        )
        process_github_daily_push_events(day=day)
        return func.HttpResponse('{"output":"This HTTP triggered function executed."}',
                                 status_code=status_code)
    except Exception as ex:
        ex_message = (f'Exception {ex} \n'
                      f'{"".join(tb.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))}')
        log.error(ex_message)
        return func.HttpResponse(ex_message, status_code=500)
