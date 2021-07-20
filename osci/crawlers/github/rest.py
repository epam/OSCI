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
from typing import NamedTuple, Optional, List, Any, Dict

import datetime
import requests
import logging
import time

from requests.structures import CaseInsensitiveDict

log = logging.getLogger(__name__)


class GithubArchiveRest(requests.Session):
    BASE_URL = 'https://data.gharchive.org/'

    @staticmethod
    def _get_hour_file_name(date: datetime.datetime) -> str:
        return f'{date.strftime("%Y-%m-%d")}-{date.hour}.json.gz'

    def _get_hour_url(self, file_name: str) -> str:
        return self.BASE_URL + file_name

    def get_hourly_events(self, date: datetime.datetime) -> bytes:
        log.info(f'Load events for date: {date}')
        file_name = self._get_hour_file_name(date=date)
        response = self.get(self._get_hour_url(file_name=file_name))
        if response.status_code == 200:
            return response.content


class RequestsLimit(NamedTuple):
    requests_limit: Optional[int]
    requests_remaining: Optional[int]
    limit_reset_time: Optional[datetime.datetime]


class GithubRest(requests.Session):
    """Github Rest Implementation"""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

    base_url = 'https://api.github.com'
    repos_url = base_url + '/repos'

    def __init__(self, token: str, wait_til_limits: bool = True):
        """Github api rest session constructor

        :param token: github api access token
        :param wait_til_limits: wait reset limits time and retry request
        """
        super().__init__()
        self.token = token
        self.limits = RequestsLimit(None, None, None)
        self.wait_til_limits = wait_til_limits

    def request(self, method, url, **kwargs) -> requests.Response:
        """Override request method to patch requests headers and parse response headers"""

        resp = self.__make_request(method=method, url=url, **kwargs)

        if self.wait_til_limits and resp.status_code == 403 and self.limits.limit_reset_time is not None:
            wait: datetime.timedelta = self.limits.limit_reset_time - datetime.datetime.now()
            log.warning(f'{method} response [{resp.status_code}]'
                        f'remaining_retries={self.limits.requests_remaining} '
                        f'Wait til {self.limits.limit_reset_time} ({wait})'
                        f'url=`{url}`')

            time.sleep(wait.total_seconds())

            log.debug(f"Retry making request to Github API method={method}, url={url}, kwargs={kwargs} "
                      f"after reset limits")

            resp = self.__make_request(method=method, url=url, **kwargs)
        return resp

    def __make_request(self, method, url, **kwargs) -> requests.Response:
        log.debug(f"Make request to Github API method={method}, url={url}, kwargs={kwargs}")

        kwargs['headers'] = {**kwargs.get('headers', {}), **{'Authorization': f'token {self.token}'}}

        resp = super().request(method=method, url=url, **kwargs)
        self.limits = self.__get_limits(resp.headers)

        log.debug(f"Get response[{resp.status_code}] from Github API  method={method}, url={url}, kwargs={kwargs}")
        return resp

    def _get_repo_url(self, repo_name):
        """Generates repository url"""
        return f'{self.repos_url}/{repo_name}'

    def _get_repo_events_url(self, repo_name):
        """Generates repository events url"""
        return f'{self._get_repo_url(repo_name)}/events'

    @staticmethod
    def __get_limits(headers) -> RequestsLimit:
        """Parse limits from response header"""

        def __parse_int(value: str) -> Optional[int]:
            """Parse int if not None"""
            try:
                return int(value)
            except Exception as ex:
                log.warning(f'Error parse `{value}` to int. Exception: {ex}')
                return

        def __parse_datetime(value: str) -> Optional[datetime.datetime]:
            """Parse datetime if not None"""
            value = __parse_int(value)
            if value is None:
                return
            try:
                return datetime.datetime.fromtimestamp(value)
            except Exception as ex:
                log.warning(f'Error parse `{value}` to datetime. Exception: {ex}')
                return

        return RequestsLimit(requests_limit=__parse_int(headers.get('X-RateLimit-Limit')),
                             requests_remaining=__parse_int(headers.get('X-RateLimit-Remaining')),
                             limit_reset_time=__parse_datetime(headers.get('X-RateLimit-Reset')))

    def get_repository_events(self, repo_name: str) -> List[dict]:
        """Get events in repository from API

        :param repo_name: repository name
        :return:
        """
        log.info(f'Get events in repository {repo_name}')
        resp = self.request(method=self.GET, url=self._get_repo_events_url(repo_name=repo_name))
        try:
            if resp.status_code == 200:
                return resp.json()
        except Exception as ex:
            log.warning(f'Exception on parse events in repository {repo_name}: {ex}')
        log.warning(f'Empty response on events in repository {repo_name}')
        return []

    def get_repository(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Get repository information from API

        :param repo_name: repository name
        :return:
        """
        log.info(f'Get repository {repo_name} information')
        resp = self.request(method=self.GET, url=self._get_repo_url(repo_name=repo_name))
        try:
            if resp.status_code == 200:
                return resp.json()
        except Exception as ex:
            log.warning(f'Exception on parse response on getting repository {repo_name}: {ex}')
        log.warning(f'Empty response on getting repository {repo_name}')
