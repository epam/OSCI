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
import zipfile

from file_loader import upload_files_from_directory
from sql_runner import run_query_from_file


class IntegrationTest(unittest.TestCase):
    FIXTURE_FOLDER = 'fixtures'
    TMP_FOLDER = 'resources'
    TEST_DB_NAME = 'test_db'

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(cls.TMP_FOLDER):
            os.mkdir(cls.TMP_FOLDER)
        path = os.path.join(cls.FIXTURE_FOLDER, 'create_test_db.sql')
        run_query_from_file('master', path)
        path = os.path.join(os.path.abspath(os.path.join("..", os.pardir)), 'SQL_queries', 'service_queries',
                            'create_empty_tables.sql')
        run_query_from_file(database=cls.TEST_DB_NAME, path_to_file=path)

    def _unzip_test_data(self):
        with zipfile.ZipFile(os.path.join(self.FIXTURE_FOLDER, 'data.zip'), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(self.TMP_FOLDER))

    def test_upload_files_from_directory(self):
        self._unzip_test_data()
        path = os.path.join(self.TMP_FOLDER)
        upload_files_from_directory(path, database=self.TEST_DB_NAME)
        path = os.path.join(os.path.abspath(os.path.join("..", os.pardir)), 'SQL_queries', 'service_queries',
                            'create_filtered_table.sql')
        run_query_from_file(database=self.TEST_DB_NAME, path_to_file=path)
        path = os.path.join(os.path.abspath(os.path.join("..", os.pardir)), 'SQL_queries', 'reports',
                            'top_30_commits_ranking.sql')
        result = run_query_from_file(database=self.TEST_DB_NAME, path_to_file=path)
        self.assertEqual(tuple(result[0]), ('Travis CI', 1))

    @classmethod
    def tearDownClass(cls):
        path = os.path.join(cls.FIXTURE_FOLDER, 'clear_test_db.sql')
        run_query_from_file(database='master', path_to_file=path)


if __name__ == '__main__':
    unittest.main()
