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
from osci.jobs.contributors_ranking import ContributorsRankingJob
from osci.jobs.contributors_repos_ranking import ContributorsReposRankingJob
from osci.jobs.month_by_month_commits_amount import MonthByMonthCommitsJob
from osci.jobs.repositories_ranking import ReposRankingJob

from osci.actions import Action, ActionParam
from osci.actions.consts import get_default_from_day, get_default_to_day
from osci.datalake import DatePeriodType


class CompanyContributorsRankingAction(Action):
    """Count employees commits"""
    params = (
        ActionParam(name='company', type=str, required=True, short_name='c', description='Company name'),
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day'),
        ActionParam(name='date_period', type=str, required=False,
                    short_name='dp', description='data period: day, month or year',
                    default=DatePeriodType.YTD, choices=DatePeriodType.all),
        ActionParam(name='from_day', type=datetime, required=False, short_name='fd',
                    description=f'Optional parameter will be ignored for no `DTD` time period.'),
    )

    @classmethod
    def name(cls) -> str:
        return 'company-contributors-ranking'

    def _execute(self, company: str, to_day: datetime, date_period: str, from_day: datetime):
        ContributorsRankingJob(date_period_type=date_period, company=company).run(to_date=to_day, from_date=from_day)


class CompanyContributorsReposRankingAction(Action):
    """Count employees repos commits"""
    params = (
        ActionParam(name='company', type=str, required=True, short_name='c', description='Company name', default=''),
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day',
                    default=get_default_to_day()),
        ActionParam(name='date_period', type=str, required=False,
                    short_name='dp', description='data period: day, month or year',
                    default=DatePeriodType.YTD, choices=DatePeriodType.all),
        ActionParam(name='from_day', type=datetime, required=False, short_name='fd',
                    description=f'Optional parameter will be ignored for no `DTD` time period.',
                    default=get_default_from_day()),
    )

    @classmethod
    def name(cls) -> str:
        return 'company-contributors-repos-ranking'

    def _execute(self, company: str, to_day: datetime, date_period: str, from_day: datetime):
        ContributorsReposRankingJob(date_period_type=date_period, company=company).run(to_date=to_day,
                                                                                       from_date=from_day)


class CompanyMonthByMonthCommitsAmountAction(Action):
    """Get month-by-month amount of commits"""
    params = (
        ActionParam(name='company', type=str, required=True, short_name='c', description='Company name', default=''),
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day',
                    default=get_default_to_day()),
    )

    @classmethod
    def name(cls) -> str:
        return 'company-month-by-month-commits-amount'

    def _execute(self, company: str, to_day: datetime):
        MonthByMonthCommitsJob(date_period_type=DatePeriodType.YTD, company=company).run(to_date=to_day)


class CompanyReposRankingAction(Action):
    """Get amount of repos commits"""
    params = (
        ActionParam(name='company', type=str, required=True, short_name='c', description='Company name', default=''),
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day',
                    default=get_default_to_day()),
        ActionParam(name='date_period', type=str, required=False,
                    short_name='dp', description='data period: day, month or year',
                    default=DatePeriodType.YTD, choices=DatePeriodType.all),
        ActionParam(name='from_day', type=datetime, required=False, short_name='fd',
                    description=f'Optional parameter will be ignored for no `DTD` time period.',
                    default=get_default_from_day()),
    )

    @classmethod
    def name(cls) -> str:
        return 'company-repos-ranking'

    def _execute(self, company: str, to_day: datetime, date_period: str, from_day: datetime):
        ReposRankingJob(date_period_type=date_period, company=company).run(to_date=to_day, from_date=from_day)


class DailyCompanyRankingsAction(Action):
    params = (
        ActionParam(name='company', type=str, required=True, short_name='c', description='Company name', default=''),
        ActionParam(name='to_day', type=datetime, required=True, short_name='td', description='till this day',
                    default=get_default_to_day()),
    )

    @classmethod
    def name(cls) -> str:
        return 'daily-company-rankings'

    def _execute(self, company: str, to_day: datetime):
        for date_period in [DatePeriodType.YTD, DatePeriodType.MTD]:
            company_contributors_ranking_job = ContributorsRankingJob(date_period_type=date_period, company=company)
            company_contributors_repos_ranking_job = ContributorsReposRankingJob(date_period_type=date_period,
                                                                                 company=company)
            company_repos_ranking_job = ReposRankingJob(date_period_type=date_period, company=company)

            commits = company_contributors_ranking_job.extract(to_date=to_day).cache()

            company_contributors_ranking_job.load(df=company_contributors_ranking_job.transform(commits), date=to_day)
            company_contributors_repos_ranking_job.load(df=company_contributors_repos_ranking_job.transform(commits),
                                                        date=to_day)
            company_repos_ranking_job.load(df=company_repos_ranking_job.transform(commits), date=to_day)

        company_month_by_month_commits_amount_job = MonthByMonthCommitsJob(date_period_type=DatePeriodType.YTD,
                                                                           company=company)
        company_month_by_month_commits_amount_job.load(
            df=company_month_by_month_commits_amount_job.transform(commits),
            date=to_day
        )
