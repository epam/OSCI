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
import logging
import click

from datetime import datetime

from __app__.match_company.process import process_github_daily_push_events as github_daily_push_events
from cli.consts import DAY_FORMAT, DEFAULT_DAY

log = logging.getLogger(__name__)


@click.group()
def cli():
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.INFO)


@cli.command()
@click.option('--day', '-d',
              default=DEFAULT_DAY, type=click.DateTime(formats=[DAY_FORMAT]),
              help=f'The date format "{DAY_FORMAT}", default: `{DEFAULT_DAY}`')
def process_github_daily_push_events(day: datetime):
    github_daily_push_events(day=day)
