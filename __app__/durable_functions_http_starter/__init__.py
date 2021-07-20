import datetime
import logging
import re

import azure.functions as func
from azure.durable_functions import DurableOrchestrationClient

DAY_FORMAT = "%Y-%m-%d"
DEFAULT_DAY = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(DAY_FORMAT)


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = DurableOrchestrationClient(starter)
    logging.info(f"Request url: {req.url}")
    base_url = re.search("(?P<url>https?://[^\s]+api)", req.url).group("url")
    function_name = req.route_params["function"]
    url_params = '&'.join(f'{k}={v}' for k, v in req.params.items())
    uri = f'{base_url}/actions/{function_name}?{url_params}'

    instance_id = await client.start_new(orchestration_function_name=req.route_params["orchestrator"],
                                         instance_id=None, client_input=uri)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    return client.create_check_status_response(req, instance_id)
