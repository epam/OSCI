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

from functools import reduce
from typing import Iterable, Tuple
from datetime import datetime

import pandas as pd

SOLUTIONS_HUB_ROWS_LIMIT = 100


def get_osci_ranking_change_report(old_report: pd.DataFrame, new_report: pd.DataFrame,
                                   company_field: str,
                                   active_contributors_field: str, active_contributors_change_field: str,
                                   total_community_field: str, total_community_change_field: str,
                                   rank_field: str, rank_change_field: str) -> pd.DataFrame:
    """Get difference between two OSCI Ranking (for two days or months or years, etc)

    :param old_report: OSCI ranking
    :param new_report: OSCI ranking
    :param company_field: company column name
    :param active_contributors_field: active contributors column name
    :param active_contributors_change_field: active contributors change column name
    :param total_community_field: total community column name
    :param total_community_change_field: total community change column name
    :param rank_field: ranking index column name
    :param rank_change_field: ranking index change column name
    :return: OSCI ranking change report
    """
    old_suffix = '_old'

    df = old_report.merge(new_report,
                          on=company_field,
                          how='outer',
                          suffixes=(old_suffix, '')
                          ).dropna(subset=[f'{rank_field}'])
    col_pairs = (
        (rank_field, rank_change_field),
        (active_contributors_field, active_contributors_change_field),
        (total_community_field, total_community_change_field),
    )
    for col, change_col in col_pairs:
        df[change_col] = df[col] - df[f'{col}{old_suffix}']

    df = df[[
        rank_field, rank_change_field,
        company_field,
        active_contributors_field, active_contributors_change_field,
        total_community_field, total_community_change_field,
    ]].sort_values(by=rank_field)
    df[rank_field] = df[rank_field].astype(int)

    return df.set_index(rank_field)


def get_contributors_ranking_mbm_change_report(reports: Iterable[Tuple[datetime, pd.DataFrame]],
                                               contributor_field: str,
                                               commits_amount_field: str) -> pd.DataFrame:
    """Creates a combined report, that shows the difference between several contributors rankings

    :param reports: collection of datatime and pandas DataFrame objects
    :param contributor_field: contributor column name
    :param commits_amount_field: amount of commits column name
    """
    df_list = []
    for report in reports:
        tmp_df = pd \
            .pivot_table(report[1],
                         values=[commits_amount_field, ],
                         index=[report[1].index.values, contributor_field]) \
            .rename(columns={commits_amount_field: datetime.strftime(report[0], '%b')}) \
            .reset_index(contributor_field)
        df_list.append(tmp_df)
    df = reduce(lambda x, y: pd.merge(x, y, how='outer', on=contributor_field), df_list) \
        .sort_values(by=contributor_field).fillna(0)
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)
    df['Total'] = df.sum(axis=1)
    return df
