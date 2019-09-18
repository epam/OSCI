import os
import unittest

import mock

from file_loader import worker
from utils import unpack_file
from shutil import copy2


class TestModules(unittest.TestCase):
    FIXTURE_FOLDER = 'fixtures'
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
