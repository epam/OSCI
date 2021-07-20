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
from pathlib import Path


from .base import BlobArea
from osci.datalake.base import BaseWebArea

from typing import Union
from functools import reduce

import logging

log = logging.getLogger(__name__)


class BlobWebArea(BaseWebArea, BlobArea):
    AREA_CONTAINER = 'data'

    def _join_paths(self, *paths: str, **kwargs) -> str:
        return reduce(lambda parent, child: f'{parent}/{child}', paths)

    def _save_json(self, path: str, json_data: str):
        self.write_string_to_file(path=path, data=json_data, content_type='application/json')

    @property
    def osci_ranking_dir(self) -> Union[str, Path]:
        return self._osci_ranking_dir_name

