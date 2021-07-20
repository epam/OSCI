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
from datetime import datetime
from osci.crawlers.github.gharchive import get_github_daily_push_events


class GithubDailyPushEventAction(Action):
    """Load push event commits from Github"""

    @classmethod
    def help_text(cls) -> str:
        return "Command for downloading daily push event commits from Github"

    @classmethod
    def name(cls):
        return 'get-github-daily-push-events'

    def _execute(self, day: datetime):
        return get_github_daily_push_events(day=day)
