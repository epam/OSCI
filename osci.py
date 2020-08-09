"""Copyright since 2020, EPAM Systems

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
import logging

from cli import company_rankers
from cli import osci_rankers
from cli import match_company
from cli import gharchive
from cli import load_osci_ranking_to_bq
from cli import osci_change_report

cli = click.CommandCollection(sources=[
    match_company.cli,
    osci_rankers.cli,
    company_rankers.cli,
    gharchive.cli,
    load_osci_ranking_to_bq.cli,
    osci_change_report.cli
])

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
    cli()
