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
from osci.actions import Action, ActionParam
from osci.publishing import load_osci_commits_ranking_to_bq
from osci.datalake import DatePeriodType
from typing import Dict, Any
import datetime


class LoadOSCICommitsRankingToBQAction(Action):
    params = Action.params + (
        ActionParam(name='date_period', type=str, required=False,
                    short_name='dp', description='data period: day, month or year',
                    default=DatePeriodType.YTD, choices=DatePeriodType.all),
    )

    @classmethod
    def name(cls) -> str:
        return "load-osci-commits-ranking-to-big-query"

    def _execute(self, day: datetime.datetime, date_period: str) -> Dict[str, Dict[str, Any]]:
        table = load_osci_commits_ranking_to_bq(date=day, date_period=date_period)
        return {'table': {'id': table.table_id, 'rows': table.num_rows}}
