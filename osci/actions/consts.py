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
import datetime

DAY_FORMAT = "%Y-%m-%d"


def get_default_day() -> str:
    return datetime.datetime(year=datetime.datetime.now().year, month=1, day=1).strftime(DAY_FORMAT)


def get_default_from_day() -> str:
    return get_default_day()


def get_default_to_day() -> str:
    return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(DAY_FORMAT)
