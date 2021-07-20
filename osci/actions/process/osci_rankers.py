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
from datetime import datetime
from osci.actions import Action, ActionParam
from osci.actions.consts import get_default_from_day, get_default_to_day

from osci.datalake import DatePeriodType
from osci.jobs.osci_ranking import OSCIRankingJob
from osci.jobs.osci_licenses import OSCILicensesJob
from osci.jobs.osci_commits_ranking import OSCICommitsRankingJob
from osci.jobs.osci_languages import OSCILanguagesJob
from osci.jobs.osci_contributors_ranking import OSCIContributorsRankingJob


class OSCICommitsRankingAction(Action):
    """Get company amount of commits"""
    params = (
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day',
                    default=get_default_to_day()),
        ActionParam(name='date_period', type=str, required=False,
                    short_name='dp', description='data period: day, month or year',
                    default=DatePeriodType.YTD, choices=DatePeriodType.all),
        ActionParam(name='from_day', type=datetime, required=False, short_name='fd',
                    description=f'Optional parameter will be ignored for no `DTD` time period.'),
    )

    @classmethod
    def name(cls) -> str:
        return 'osci-commits-ranking'

    def _execute(self, to_day: datetime, date_period: str, from_day: datetime):
        OSCICommitsRankingJob(date_period_type=date_period).run(to_date=to_day, from_date=from_day)


class OSCIContributorsRankingAction(Action):
    """Generates OSCI contributors ranking"""
    params = (
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day'),
    )

    @classmethod
    def name(cls) -> str:
        return 'osci-contributors-ranking'

    def _execute(self, to_day: datetime):
        OSCIContributorsRankingJob(date_period_type=DatePeriodType.YTD).run(to_date=to_day)


class OSCILanguagesAction(Action):
    """Generates OSCI commits enriched with languages"""
    params = (
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day'),
    )

    @classmethod
    def name(cls) -> str:
        return 'osci-languages'

    def _execute(self, to_day: datetime):
        OSCILanguagesJob(date_period_type=DatePeriodType.YTD).run(to_date=to_day)


class OSCILicensesAction(Action):
    """Generates OSCI commits enriched with licenses"""
    params = (
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day'),
    )

    @classmethod
    def name(cls) -> str:
        return 'osci-licenses'

    def _execute(self, to_day: datetime):
        OSCILicensesJob(date_period_type=DatePeriodType.YTD).run(to_date=to_day)


class OSCIRankingAction(Action):
    """Companies rank with employees activity"""

    params = (
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day'),
        ActionParam(name='date_period', type=str, required=False,
                    short_name='dp', description='data period: day, month or year',
                    default=DatePeriodType.YTD, choices=DatePeriodType.all),
        ActionParam(name='from_day', type=datetime, required=False, short_name='fd',
                    description=f'Optional parameter will be ignored for no `DTD` time period.'),
    )

    @classmethod
    def name(cls) -> str:
        return 'osci-ranking'

    def _execute(self, to_day: datetime, date_period: str, from_day: datetime):
        OSCIRankingJob(date_period_type=date_period).run(to_date=to_day, from_date=from_day)
