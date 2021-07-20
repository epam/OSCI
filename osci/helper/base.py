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
import pandas as pd
from typing import Dict, List, Any, Mapping


def base_map_generator(df: pd.DataFrame, group_by_column: str, nested_columns: List[str],
                       rename_columns: Dict[str, str] = None) -> Mapping[str, List[Dict[str, Any]]]:
    return {group_by_column: group_df[nested_columns].rename(columns=rename_columns or dict()).to_dict('records')
            for group_by_column, group_df in df.groupby([group_by_column])}
