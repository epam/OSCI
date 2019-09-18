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


import pyodbc

from secrets import Server, PWD, UID


class DBConnector:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   'Server=%s;'
                                   'Database=%s;'
                                   'UID=%s;'
                                   'PWD=%s;'
                                   'Trusted_Connection=yes;' % (Server, self.db_name, UID, PWD), autocommit=True)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
