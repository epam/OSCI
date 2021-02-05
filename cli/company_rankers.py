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

import click
import datetime
import logging

from __app__.datalake import DatePeriodType
from __app__.jobs.contributors_ranking import ContributorsRankingJob
from __app__.jobs.contributors_repos_ranking import ContributorsReposRankingJob
from __app__.jobs.month_by_month_commits_amount import MonthByMonthCommitsJob
from __app__.jobs.repositories_ranking import ReposRankingJob

from cli.consts import DAY_FORMAT, DEFAULT_FROM_DAY, DEFAULT_TO_DAY

log = logging.getLogger(__name__)


@click.group()
def cli():
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.INFO)


@cli.command()
@click.option('--company', '-c',
              default='', type=str,
              help='Company name')
@click.option('--to_day', '-td',
              default=DEFAULT_TO_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_TO_DAY}`')
@click.option('--date_period', '-dp',
              default=DatePeriodType.YTD,
              type=click.Choice(DatePeriodType.all, case_sensitive=False))
@click.option('--from_day', '-fd',
              default=DEFAULT_FROM_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'Optional parameter will be ignored for no `DTD` time period. '
                   f'The date format "{DAY_FORMAT}", default: `{DEFAULT_FROM_DAY}`')
def company_contributors_ranking(company: str, to_day: datetime, date_period: str, from_day: datetime):
    ContributorsRankingJob(date_period_type=date_period, company=company).run(to_date=to_day, from_date=from_day)


@cli.command()
@click.option('--company', '-c',
              default='', type=str,
              help='Company name')
@click.option('--to_day', '-td',
              default=DEFAULT_TO_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_TO_DAY}`')
@click.option('--date_period', '-dp',
              default=DatePeriodType.YTD,
              type=click.Choice(DatePeriodType.all, case_sensitive=False))
@click.option('--from_day', '-fd',
              default=DEFAULT_FROM_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'Optional parameter will be ignored for no `DTD` time period. '
                   f'The date format "{DAY_FORMAT}", default: `{DEFAULT_FROM_DAY}`')
def company_contributors_repos_ranking(company: str, to_day: datetime, date_period: str, from_day: datetime):
    ContributorsReposRankingJob(date_period_type=date_period, company=company).run(to_date=to_day, from_date=from_day)


@cli.command()
@click.option('--company', '-c',
              default='', type=str,
              help='Company name')
@click.option('--to_day', '-td',
              default=DEFAULT_TO_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_TO_DAY}`')
@click.option('--date_period', '-dp',
              default=DatePeriodType.YTD,
              type=click.Choice(DatePeriodType.all, case_sensitive=False))
@click.option('--from_day', '-fd',
              default=DEFAULT_FROM_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'Optional parameter will be ignored for no `DTD` time period. '
                   f'The date format "{DAY_FORMAT}", default: `{DEFAULT_FROM_DAY}`')
def company_repos_ranking(company: str, to_day: datetime, date_period: str, from_day: datetime):
    ReposRankingJob(date_period_type=date_period, company=company).run(to_date=to_day, from_date=from_day)


@cli.command()
@click.option('--company', '-c',
              default='', type=str,
              help='Company name')
@click.option('--to_day', '-td',
              default=DEFAULT_TO_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_TO_DAY}`')
def company_month_by_month_commits_amount(company: str, to_day: datetime):
    MonthByMonthCommitsJob(date_period_type=DatePeriodType.YTD, company=company).run(to_date=to_day)


@cli.command()
@click.option('--company', '-c',
              default='', type=str,
              help='Company name')
@click.option('--to_day', '-td',
              default=DEFAULT_TO_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_TO_DAY}`')
def daily_company_rankings(company: str, to_day: datetime):
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


if __name__ == '__main__':
    cli()
