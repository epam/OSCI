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

import re
import pandas as pd


def filter_projects(df: pd.DataFrame, projects_filter_list: list, commits_amount_field: str,
                    repo_name_field: str) -> pd.DataFrame:
    """Returns DataFrame with filtered projects

    :param df: input DataFrame
    :param projects_filter_list: list of required company projects
    :param commits_amount_field: commits column name
    :param repo_name_field: repository column name
    :return:
    """
    if df.size == 0:
        return pd.DataFrame(columns=['Project', 'Description', commits_amount_field, 'Total_%'])
    df['Total_%'] = df[commits_amount_field] / df[commits_amount_field].sum() * 100
    df[['Project', 'Description']] = df[repo_name_field].apply(
        lambda v: pd.Series(_replace(v, projects_filter_list), dtype=str))
    df = df.groupby(['Project', 'Description']).sum().sort_values([commits_amount_field], ascending=False).reset_index()
    return df


def _replace(value: str, companies: list):
    for data in companies:
        for string in data.get('regex'):
            if re.findall(string, value, re.IGNORECASE):
                return [data.get('Project'), data.get('description')]

