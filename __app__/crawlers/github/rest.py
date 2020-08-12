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
import datetime
import requests
import logging

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
