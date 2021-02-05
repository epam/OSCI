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

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

if 'dbutils' in globals():
    log.debug('Variable `dbutils` in memory. Try to setup config with `dbutils`')
    from __app__.config import Config, FileSystemType

    config = Config(dbutils=dbutils)

    if 'spark' in globals():
        log.debug('Variable `spark` in memory.')
        from __app__.jobs.session import Session

        Session(spark_session=spark)
        if Config().file_system_type == FileSystemType.blob:
            print('FS CONF', f'fs.azure.account.key.{Config().file_system.staging_props.get("storage_account_name")}.'
                             f'blob.core.windows.net', Config().file_system.staging_props.get('storage_account_key')
                  )
            spark.conf.set(
                f'fs.azure.account.key.{Config().file_system.staging_props.get("storage_account_name")}.'
                f'blob.core.windows.net',
                Config().file_system.staging_props.get('storage_account_key')
            )

from cli import company_rankers
from cli import osci_rankers
from cli import match_company
from cli import gharchive
from cli import load_osci_ranking_to_bq
from cli import load_osci_commits_ranking_to_bq
from cli import osci_change_report
from cli import company_commits
from cli import generate_email
from cli import find_new_repos_and_commiters
from cli import load_repositories
from cli import get_daily_active_repositories
from cli import filter_unlicensed

cli = click.CommandCollection(sources=[
    match_company.cli,
    osci_rankers.cli,
    company_rankers.cli,
    gharchive.cli,
    load_osci_ranking_to_bq.cli,
    company_commits.cli,
    osci_change_report.cli,
    generate_email.cli,
    load_osci_commits_ranking_to_bq.cli,
    find_new_repos_and_commiters.cli,
    load_repositories.cli,
    get_daily_active_repositories.cli,
    filter_unlicensed.cli,
])

if __name__ == '__main__':
    cli(standalone_mode=False)
