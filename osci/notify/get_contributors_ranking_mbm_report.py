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

from osci.datalake.schemas.public import ContributorsRankingMBMReportSchema


def get_contributors_ranking_mbm_change_report(reports: Iterable[Tuple[datetime, pd.DataFrame]],
                                               contributor_field: str,
                                               commits_amount_field: str) -> pd.DataFrame:
    """Creates a combined report, that shows the difference between several contributors rankings

    :param reports: collection of datatime and pandas DataFrame objects
    :param contributor_field: contributor column name
    :param commits_amount_field: amount of commits column name
    """
    report = pd.DataFrame(columns=ContributorsRankingMBMReportSchema.required)
    df_list = []
    for item in reports:
        tmp_df = pd \
            .pivot_table(item[1],
                         values=[commits_amount_field, ],
                         index=[item[1].index.values, contributor_field]) \
            .rename(columns={commits_amount_field: datetime.strftime(item[0], '%b')}) \
            .reset_index(contributor_field)
        df_list.append(tmp_df)
    df = reduce(lambda x, y: pd.merge(x, y, how='outer', on=contributor_field), df_list) \
        .sort_values(by=contributor_field).fillna(0)
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)
    df[ContributorsRankingMBMReportSchema.total] = df.sum(axis=1)
    df = df.sort_values(ContributorsRankingMBMReportSchema.total, ascending=False)
    for column in report.columns:
        if column in df.columns:
            report[column] = df[column]
    return report
