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
from typing import Optional
from datetime import datetime, timedelta

import pandas as pd
import io
import logging

log = logging.getLogger(__name__)


class MetaSingleton(type):
    """Metaclass for create singleton"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
            log.debug(f'Create new {cls}')
        return cls._instances[cls]


def get_pandas_data_frame_info(df: pd.DataFrame) -> str:
    """Returns dataframe info as string

    :param df: pandas dataframe
    :return: dataframe info as string
    """
    with io.StringIO() as buf:
        df.info(buf=buf)
        return buf.getvalue()


def get_azure_blob_connection_string(account_name: str, account_key: str) -> str:
    """Generates azure blob storage connection string by account_name and account_key

    :param account_name: account name
    :param account_key: sas token
    :return: azure blob storage connection string
    """
    return "DefaultEndpointsProtocol=https;" \
           f"AccountName={account_name};" \
           f"AccountKey={account_key};" \
           "EndpointSuffix=core.windows.net"


def normalize_company(name: str) -> str:
    """Generate company file name safety string
    Replace all non-alpha and non-numeric with '_'

    :param name: original string
    :return: company file name safety string
    """
    return ''.join((symbol if symbol.isalnum() else '_').lower() for symbol in str(name))


def parse_date_field(date_field_value: Optional[str] = None) -> Optional[datetime]:
    return date_field_value \
        if date_field_value is None \
        else datetime.fromisoformat(date_field_value.replace('Z', ''))


def get_compared_date(day: datetime):
    if day.month == 1:
        return datetime(year=day.year, month=day.month, day=1)
    return datetime(year=day.year, month=day.month, day=1) - timedelta(days=1)
