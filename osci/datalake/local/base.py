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

from osci.datalake.base import BaseDataLakeArea

from pathlib import Path
from typing import Iterator, Union
from io import BytesIO


class LocalSystemArea(BaseDataLakeArea):
    BASE_PATH = Path(__file__).parent.parent.parent.resolve() / 'data'
    FS_PREFIX = 'file'
    BASE_AREA_DIR = None

    def __init__(self, base_path=BASE_PATH, base_area_dir=BASE_AREA_DIR):
        super().__init__()
        self.BASE_PATH = Path(base_path)
        self.BASE_AREA_DIR = base_area_dir
        print(self, base_path, base_area_dir)

    def add_fs_prefix(self, path: Union[Path, str]) -> str:
        return f'{self.FS_PREFIX}:///{path}'

    def add_fs_absolute_prefix(self, path):
        return f'{self.FS_PREFIX}:///{Path(path).absolute()}'

    @staticmethod
    def _get_paths(dir_path: Union[str, Path], file_pattern='*.parquet') -> Iterator[Path]:
        return Path(dir_path).rglob(file_pattern)

    @property
    def _github_events_commits_base(self) -> Union[str, Path]:
        return self.BASE_PATH / self.BASE_AREA_DIR / 'github' / 'events' / 'push'

    @property
    def _github_raw_events_commits_base(self) -> Union[str, Path]:
        return self.BASE_PATH / self.BASE_AREA_DIR / 'github' / 'raw-events' / 'push'

    @property
    def _github_repositories_base(self) -> Path:
        return self.BASE_PATH / self.BASE_AREA_DIR / 'github' / 'repository'

    def write_bytes_to_file(self, path: str, buffer: BytesIO):
        with open(path, 'wb') as file:
            file.write(buffer.getvalue())
