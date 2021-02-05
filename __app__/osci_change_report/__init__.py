from .process import get_change_report
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
        get_change_report(date=datetime.datetime.strptime(
            get_req_param(req, 'date', default=DEFAULT_DAY),
            DAY_FORMAT
        ))
        return func.HttpResponse('{"output":"This HTTP triggered function executed."}',
                                 status_code=status_code)
    except Exception as ex:
        log.error(f'Exception {ex}')
        status_code = 500
        return func.HttpResponse(f"Exception {ex}"
                                 f"{''.join(tb.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))}",
                                 status_code=status_code)
