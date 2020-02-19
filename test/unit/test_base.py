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


import os
import unittest
from pathlib import Path

import mock

from osci.file_loader import worker
from osci.utils import unpack_file
from shutil import copy2


class TestModules(unittest.TestCase):
    CWD = Path(__file__).parent.resolve()
    FIXTURE_FOLDER = CWD / 'fixtures'
    TMP_FOLDER = 'resources'
    ARCHIVE_FILE = '2019-01-01-23.json.gz'
    FILE = '2019-01-01-23.json'
    FORMATTED_FILE = '2019-01-01-23-formatted.json'

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(cls.TMP_FOLDER):
            os.mkdir(cls.TMP_FOLDER)

    @staticmethod
    def _mock_response(status=200, content=None, json_data=None, raise_for_status=None):
        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.status_code = status
        mock_resp.content = content
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp

    @mock.patch('requests.get')
    def test_worker(self, mock_get):
        with open(os.path.join(self.FIXTURE_FOLDER, self.ARCHIVE_FILE), 'rb') as file:
            mock_resp = self._mock_response(content=file.read())
            mock_get.return_value = mock_resp
            worker(work_dir=self.TMP_FOLDER,
                   year='2019',
                   month='01',
                   day='01',
                   hour='23'
                   )
        self.assertTrue(os.path.isfile(os.path.join(self.TMP_FOLDER, self.FORMATTED_FILE)))

    def test_unpack_file(self):
        copy2(os.path.join(self.FIXTURE_FOLDER, self.ARCHIVE_FILE), self.TMP_FOLDER)
        files = os.listdir(self.TMP_FOLDER)
        for file in files:
            if file.endswith(".gz"):
                unpack_file(os.path.join(self.TMP_FOLDER, file))
                self.assertTrue(os.path.isfile(os.path.join(self.TMP_FOLDER, self.FILE)))
                os.remove(os.path.join(self.TMP_FOLDER, self.FILE))

    @classmethod
    def tearDownClass(cls):
        files = os.listdir(cls.TMP_FOLDER)
        for file in files:
            os.remove(os.path.join(cls.TMP_FOLDER, file))
        if os.path.exists(cls.TMP_FOLDER) and not os.listdir(cls.TMP_FOLDER):
            os.rmdir(cls.TMP_FOLDER)


if __name__ == '__main__':
    unittest.main()
