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


import datetime
import os
from calendar import monthrange
from multiprocessing import cpu_count
from multiprocessing.pool import Pool

import requests

from dbconnector import DBConnector
from sql_runner import run_query_from_file, run_query
from sql_uploader import upload_to_database
from utils import format_json_file, unpack_file, clear_directory


echo = print


def get_day_data(year, month, day):
    """
    get all files per day
    :param year: required year
    :param month: required month
    :param day: required day
    """
    directory = os.path.join(year, month, day)
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        files = os.listdir(directory)
        if files is not None:
            print('Directory "{}" already exists and not empty'.format(directory))
            return
    if cpu_count() > 1:
        p = Pool(cpu_count() - 1)
    else:
        p = Pool(1)
    for hour in range(24):
        p.apply_async(worker, args=(directory, year, month, day, hour))
    p.close()
    p.join()


def worker(work_dir, year, month, day, hour):
    """
    loads from archive gharchive.org, unpack and reformat json data unit
    :param work_dir: working directory
    :param year: required year
    :param month: required month
    :param day: required day
    :param hour: required hour
    """
    url = 'https://data.gharchive.org/{}-{}-{}-{}.json.gz'.format(year, month, day, hour)
    path = os.path.join(work_dir, '{}-{}-{}-{}'.format(year, month, day, hour))
    r = requests.get(url)
    if r.status_code == 200:
        with open("".join((path, ".json.gz")), 'wb') as f:
            f.write(r.content)
        unpack_file("".join((path, ".json.gz")))
        format_json_file("".join((path, ".json")), clear_src=True)
    else:
        raise FileNotFoundError


def get_month_data(year, month, database):
    """
    get all data per required month
    :param database: target database
    :param year: required year
    :param month: required month
    """
    db_pool = Pool(1)
    days_in_month = monthrange(int(year), int(month))[1]
    for day in range(1, days_in_month + 1):
        if day < 10:
            day = str(day).zfill(2)
        get_day_data(year, month, str(day))
        folder = os.path.join(year, month, str(day))
        db_pool.apply_async(upload_files_from_directory, args=(folder, database))
    db_pool.close()
    db_pool.join()


def get_year(year, database):
    """
    loads data per certain year
    :param year: target year
    :param database: target database
    """
    date = datetime.datetime.now()
    if int(year) == date.year:
        for month in range(1, date.month):
            if month < 10:
                month = str(month).zfill(2)
            get_month_data(year=str(year), month=month, database=database)
    else:
        for month in range(1, 12 + 1):
            if month < 10:
                month = str(month).zfill(2)
            get_month_data(year=str(year), month=month, database=database)


def upload_files_from_directory(directory, database):
    """
    scans files in the directory and loads them in to database
    :param database:  target database
    :param directory: target directory
    """
    files = os.listdir(directory)
    for file in files:
        upload_to_database(os.path.join(directory, file), db_name=database)
    clear_directory(directory)


if __name__ == '__main__':
    _database = 'GitAnalytics'
    if not DBConnector(_database).exists():
        echo(f"Creating database '{_database}'..")
        run_query(
            database="master",
            query="CREATE DATABASE {0} COLLATE SQL_Latin1_General_CP1_CI_AS;".format(
                _database))
    else:
        echo(f"Using existing database '{_database}'..")

    run_query_from_file(database=_database,
                        path_to_file=os.path.join('SQL_queries', 'service_queries', 'create_empty_tables.sql'))

    get_month_data('2019', '01', database=_database)

    run_query_from_file(database=_database,
                        path_to_file=os.path.join('SQL_queries', 'service_queries', 'create_filtered_table.sql'))

