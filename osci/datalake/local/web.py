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

from .base import LocalSystemArea
from osci.datalake.base import BaseWebArea

from functools import reduce

import logging

log = logging.getLogger(__name__)


class LocalWebArea(BaseWebArea, LocalSystemArea):
    BASE_AREA_DIR = 'data'

    def _join_paths(self, *paths: Path, create_if_not_exists=False) -> Path:
        path = reduce(lambda parent, child: parent / child, paths)
        if create_if_not_exists:
            path.mkdir(parents=True, exist_ok=True)
        return path

    def _save_json(self, path: Path, json_data: str):
        with open(path, 'w') as f:
            f.write(json_data)

    @property
    def osci_ranking_dir(self) -> Path:
        return self.BASE_PATH / self.BASE_AREA_DIR / self._osci_ranking_dir_name

