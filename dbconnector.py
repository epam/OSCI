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

import sqlalchemy

from secrets import Server, PWD, UID

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"mssql+pyodbc://{UID}:{PWD}@{Server}/"
    + "{db_name}"
    + "?driver=SQL+Server&autocommit=True",
)


class DBConnector:
    def __init__(self, db_name):
        self.db_url = DATABASE_URL.format(db_name=db_name)

    def __enter__(self):
        self.engine = sqlalchemy.create_engine(self.db_url)
        self.conn = self.engine.raw_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


if __name__ == "__main__":
    # Example of connecting with FreeTDS driver on Linux
    """
    DATABASE_URL = (
        "mssql+pyodbc://sa:yourStrong(!)Password@127.0.0.1:1433/"
        + "{db_name}"
        + "?driver=FreeTDS&autocommit=True"
    ) """
    print('env DATABASE_URL=' + DATABASE_URL)
    with DBConnector("master") as conn:
        print(conn)
