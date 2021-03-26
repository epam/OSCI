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
from __app__.jobs.osci_ranking import OSCIRankingJob
from __app__.jobs.osci_licenses import OSCILicensesJob
from __app__.jobs.osci_commits_ranking import OSCICommitsRankingJob
from __app__.jobs.company_contributors_repository_commits import CompanyContributorsRepositoryCommitsJob
from __app__.jobs.osci_contributors_ranking import OSCIContributorsRankingJob

from cli.consts import DAY_FORMAT, DEFAULT_FROM_DAY, DEFAULT_TO_DAY

log = logging.getLogger(__name__)


@click.group()
def cli():
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.INFO)


@cli.command()
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
def osci_ranking(to_day: datetime, date_period: str, from_day: datetime):
    OSCIRankingJob(date_period_type=date_period).run(to_date=to_day, from_date=from_day)


@cli.command()
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
def osci_commits_ranking(to_day: datetime, date_period: str, from_day: datetime):
    OSCICommitsRankingJob(date_period_type=date_period).run(to_date=to_day, from_date=from_day)


@cli.command()
@click.option('--to_day', '-td',
              default=DEFAULT_TO_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_TO_DAY}`')
def osci_contributors_ranking(to_day: datetime):
    OSCIContributorsRankingJob(date_period_type=DatePeriodType.YTD).run(to_date=to_day)


@cli.command()
@click.option('--to_day', '-td',
              default=DEFAULT_TO_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_TO_DAY}`')
def daily_osci_rankings(to_day: datetime):
    for date_period in [DatePeriodType.YTD, DatePeriodType.MTD]:
        osci_ranking_job = OSCIRankingJob(date_period_type=date_period)
        osci_commits_ranking_job = OSCICommitsRankingJob(date_period_type=date_period)

        commits = osci_ranking_job.extract(to_date=to_day).cache()

        osci_ranking_job.load(df=osci_ranking_job.transform(commits), date=to_day)
        osci_commits_ranking_job.load(df=osci_commits_ranking_job.transform(commits), date=to_day)

        if date_period == DatePeriodType.YTD:
            company_contributors_repos = CompanyContributorsRepositoryCommitsJob(date_period_type=date_period)
            company_contributors_repos.load(company_contributors_repos.transform(commits, date=to_day), date=to_day)

            osci_contributors_ranking_job = OSCIContributorsRankingJob(date_period_type=date_period)
            osci_contributors_ranking_job.load(osci_contributors_ranking_job.transform(commits), date=to_day)

            osci_licenses_ytd = OSCILicensesJob(date_period_type=date_period)
            osci_licenses_ytd.load(osci_licenses_ytd.transform(df=commits), date=to_day)


@cli.command()
@click.option('--to_day', '-td',
              default=DEFAULT_TO_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_TO_DAY}`')
def osci_licenses(to_day: datetime):
    OSCILicensesJob(date_period_type=DatePeriodType.YTD).run(to_date=to_day)


if __name__ == '__main__':
    cli()
