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
from osci.postprocess.osci_change_report.process import get_change_report

from datetime import datetime


class OSCIChangeReportAction(Action):
    """Create report"""

    @classmethod
    def help_text(cls) -> str:
        return "Create final ranking report"

    @classmethod
    def name(cls):
        return 'get-change-report'

    def _execute(self, day: datetime):
        return get_change_report(date=day)
