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
import traceback as tb

import azure.functions as func

from __app__.utils import get_req_param

from .process import get_daily_active_repositories

DAY_FORMAT = "%Y-%m-%d"
DEFAULT_DAY = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(DAY_FORMAT)
log = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
    try:
        log.info(f"Http trigger. req.params: {req.params}")
        date = datetime.datetime.strptime(get_req_param(req, 'date', default=DEFAULT_DAY), DAY_FORMAT)
        get_daily_active_repositories(date=date)
        return func.HttpResponse('{"output":"This HTTP triggered function executed."}',
                                 status_code=200)
    except Exception as ex:
        log.error(f'Exception {ex}')
        log.exception(ex)
        return func.HttpResponse(f"This HTTP triggered function failed {ex} "
                                 f"{''.join(tb.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))}",
                                 status_code=500)
