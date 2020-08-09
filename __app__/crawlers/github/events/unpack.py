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

from gzip import decompress
from typing import Iterator

import json
import logging

log = logging.getLogger(__name__)


def decompress_json_lines(content: bytes) -> Iterator[dict]:
    json_lines = decompress(content).decode('utf-8')
    for line in json_lines.split('\n'):
        log.debug(f'Try to parse json: {line}')
        try:
            yield json.loads(line, encoding='utf-8')
        except Exception as ex:
            log.error(f'Failed to parse json: {line}. Error: {ex}')
