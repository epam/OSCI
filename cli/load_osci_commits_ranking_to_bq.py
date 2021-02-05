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

from __app__.load_osci_commits_ranking_to_bq.loader import load_osci_commits_ranking_to_bq
from __app__.datalake import DatePeriodType
from cli.consts import DEFAULT_DAY, DAY_FORMAT


@click.group()
def cli():
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)


@cli.command()
@click.option('--day', '-d',
              default=DEFAULT_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_DAY}`')
@click.option('--date_period', '-dp',
              default=DatePeriodType.YTD,
              type=click.Choice(DatePeriodType.all, case_sensitive=False))
def load_osci_commits_ranking_to_big_query(day: datetime.datetime, date_period: str):
    load_osci_commits_ranking_to_bq(date=day, date_period=date_period)


if __name__ == '__main__':
    cli()
