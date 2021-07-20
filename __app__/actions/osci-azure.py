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
from typing import Mapping, Dict
from osci.actions import Action, ListAction
from http import HTTPStatus

import azure.functions as func
import traceback as tb
import logging
import json

log = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Handle http request and run azure function handlers"""
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
    handlers: Mapping[str, Action] = {class_var.name(): class_var for class_var in Action.__subclasses__()}
    log.info(f"Find Actions subclasses: {handlers}")
    success_message = {"output": "This HTTP triggered function executed."}
    try:
        action_name = req.route_params.get('action_name', 'list')
        log.info(f"Action name: `{action_name}`")
        action = handlers.get(action_name)

        if not action:
            raise KeyError(f"Can't find required Action for `{action_name}` azure function")
        params: Dict = req.params or req.get_json()
        message = action().execute(**params) or success_message
        return func.HttpResponse(json.dumps(message), status_code=HTTPStatus.OK)
    except Exception as ex:
        ex_message = (f'Exception {ex} \n'
                      f'{"".join(tb.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))}')
        log.error(ex_message)
        return func.HttpResponse(ex_message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
