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

from dbconnector import DBConnector


def run_query_from_file(database, path_to_file):
    """
    runs query from *.sql file
    :param database: target database
    :param path_to_file: path to file with sql query
    :return: returns a table if it exists
    """
    with DBConnector(db_name=database) as conn:
        cursor = conn.cursor()
        file = open(path_to_file, 'r')
        sql = " ".join(file.readlines())
        cursor.execute(sql)
        cursor.commit()
        try:
            results = cursor.fetchall()
            return results
        except pyodbc.ProgrammingError:
            pass
        finally:
            cursor.close()


def run_query(database, query):
    """
    runs query from variable with sql code
    :param database: target database
    :param query: variable with sql code
    :return: returns a table if it exists
    """
    with DBConnector(db_name=database) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.commit()
        try:
            results = cursor.fetchall()
            return results
        except pyodbc.ProgrammingError:
            pass
        finally:
            cursor.close()
