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
from .loader import load_company_repositories_events_commits
from __app__.utils import get_req_param
from __app__.config import Config

import datetime
import logging
import azure.functions as func
import traceback as tb
import json

DAY_FORMAT = "%Y-%m-%d"
DEFAULT_DAY = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(DAY_FORMAT)
log = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
    try:
        log.info(f"Http trigger. req.params: {req.params}")
        date = datetime.datetime.strptime(get_req_param(req, 'date', default=DEFAULT_DAY), DAY_FORMAT)
        company = get_req_param(req, 'company', default=Config().default_company)
        load_company_repositories_events_commits(date=date, company=company)
        func.HttpResponse(json.dumps({'status': 'SUCCESS'}))
    except Exception as ex:
        ex_message = (f'Exception {ex} \n'
                      f'{"".join(tb.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))}')
        log.error(ex_message)
        return func.HttpResponse(ex_message, status_code=500)
