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

from .match import match_company_by_email
from typing import Iterable, Tuple

import pandas as pd
import logging

log = logging.getLogger(__name__)


def add_company_column_by_email(df: pd.DataFrame, email_field: str, company_field: str) -> pd.DataFrame:
    log.debug(f'Add company column {company_field} by field {email_field}')
    df[company_field] = df[email_field].apply(func=match_company_by_email)
    return df


def filter_out_non_company_commits(df: pd.DataFrame, company_field: str) -> pd.DataFrame:
    log.debug('Remove `null` companies')
    return df[df[company_field].notnull()]


def parse_dates(df: pd.DataFrame, datetime_field: str) -> pd.DataFrame:
    log.debug('Parse string column to datetime')
    if pd.api.types.is_datetime64_any_dtype(df[datetime_field]):
        log.warning(f'Column {datetime_field} is already type {df[datetime_field].dtype}. Nothing to do')
        return df

    if pd.api.types.is_string_dtype(df[datetime_field]):
        df[datetime_field] = pd.to_datetime(df[datetime_field])
    else:
        log.warning(f'Cannot parse to datetime column {datetime_field} with type {df[datetime_field].dtype}')
    return df


def process_push_commits(df: pd.DataFrame, email_field: str,
                         company_field: str, datetime_field: str) -> Iterable[Tuple[str, pd.DataFrame]]:
    df = add_company_column_by_email(df, email_field=email_field, company_field=company_field)
    df = filter_out_non_company_commits(df, company_field=company_field)
    df = parse_dates(df, datetime_field=datetime_field)
    log.debug(f'Group df by company field: {company_field}')
    return df.groupby(company_field)
