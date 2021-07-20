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
import logging

import pandas as pd
from typing import Iterable

from osci.notify.generate_email.consts import OSCI_REPORTS_URLS
from osci.config import Config
from osci.datalake import DataLake
from osci.notify.generate_email.email import EmailBodyTemplate
from osci.postprocess.osci_change_report.process import get_previous_date
from osci.datalake.reports.general import OSCIChangeRanking
from osci.datalake.reports.excel import OSCIChangeRankingExcel

log = logging.getLogger(__name__)


def __add_suffix(column, suffix):
    return f"{column} {suffix}"


def __cast_columns_to_int(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    return df.astype({col: 'Int64' for col in columns})


def __get_shift_up(change_ranking: pd.DataFrame, change_position_field: str) -> pd.DataFrame:
    return change_ranking[change_ranking[change_position_field] < 0].sort_values(change_position_field).head(5)


def __get_shift_down(change_ranking: pd.DataFrame, change_position_field: str) -> pd.DataFrame:
    return change_ranking[change_ranking[change_position_field] > 0].sort_values(change_position_field,
                                                                                 ascending=False).head(5)


def __add_arrows_prefix(df: pd.DataFrame, column: str):
    def get_arrow(v):
        if v == 0:
            return '—'
        arrow_down = '▼'
        arrow_up = '▲'
        arrow = arrow_down if v > 0 else arrow_up
        return f'{arrow} {abs(v)}'
    if df.empty:
        return df
    ndf = df.copy()
    ndf[column] = [get_arrow(v) for v in ndf[column]]
    return ndf


def __get_company_neighbors(df, company, company_field, rank_field, neighbors=1):
    company_rows = df[df[company_field] == company]
    if not company_rows.empty:
        position = company_rows[rank_field].array[0]
        left_border = position - neighbors
        right_border = position + neighbors
        return df[(df[rank_field] >= left_border) & (df[rank_field] <= right_border)]
    return pd.DataFrame()


def generate_email_body(date: datetime, company=Config().default_company):
    report = OSCIChangeRanking(date=date)
    company_contributors_ranking_schema = DataLake().public.schemas.company_contributors_ranking

    change_ranking = report.read().reset_index()
    change_ranking = change_ranking.rename(columns={'index': company_contributors_ranking_schema.position})
    change_ranking[company_contributors_ranking_schema.position] += 1
    change_ranking = __cast_columns_to_int(df=change_ranking,
                                           columns=[
                                               report.schema.total,
                                               report.schema.active,
                                               company_contributors_ranking_schema.position,

                                               report.schema.total_change,
                                               report.schema.active_change,
                                               report.schema.position_change,
                                           ])
    shift_up = __add_arrows_prefix(df=__get_shift_up(change_ranking=change_ranking,
                                                     change_position_field=report.schema.position_change),
                                   column=report.schema.position_change)
    shift_down = __add_arrows_prefix(df=__get_shift_down(change_ranking=change_ranking,
                                                         change_position_field=report.schema.position_change),
                                     column=report.schema.position_change)
    company_position = __add_arrows_prefix(df=__get_company_neighbors(df=change_ranking,
                                                                      company=company,
                                                                      company_field=report.schema.company,
                                                                      rank_field=company_contributors_ranking_schema.position),
                                           column=report.schema.position_change)
    DataLake().public.save_email(email_body=EmailBodyTemplate().render(
        date=date,
        compared_date=get_previous_date(date),
        shift_up=shift_up,
        shift_down=shift_down,
        company=company,
        company_position=company_position,
        solutionshub_osci_change_ranking=OSCIChangeRankingExcel(to_date=date).url,
        osci_reports_urls={name: report_cls(date=date).url for name, report_cls in OSCI_REPORTS_URLS.items()}
    ), date=date)
