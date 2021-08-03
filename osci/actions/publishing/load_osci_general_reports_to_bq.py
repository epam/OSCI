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
from osci.actions import Action
from osci.publishing import load_osci_general_reports_to_bq
from typing import Dict, Any

import datetime


class LoadOSCIGeneralReportToBQAction(Action):

    @classmethod
    def name(cls) -> str:
        return "load-osci-general-reports-to-big-query"

    def _execute(self, day: datetime.datetime) -> Dict[str, Dict[str, Any]]:
        table = load_osci_general_reports_to_bq(date=day)
        return {'table': {'id': table.table_id, 'rows': table.num_rows}}
