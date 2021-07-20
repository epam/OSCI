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
from osci.preprocess.match_company.process import process_github_daily_push_events
from osci.actions import Action
from datetime import datetime


class MatchCompanyAction(Action):
    """Enrich and filter by company"""

    @classmethod
    def help_text(cls) -> str:
        return "Command for processing daily github push events (filtering, enriching data etc)"

    @classmethod
    def name(cls):
        return 'process-github-daily-push-events'

    def _execute(self, day: datetime):
        return process_github_daily_push_events(day=day)
