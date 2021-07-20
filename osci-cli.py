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
import logging
from datetime import datetime

import click

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)

log = logging.getLogger(__name__)


if 'dbutils' in globals():
    log.debug('Variable `dbutils` in memory. Try to setup config with `dbutils`')
    from osci.config import Config, FileSystemType

    config = Config(dbutils=dbutils)

    if 'spark' in globals():
        log.debug('Variable `spark` in memory.')
        from osci.jobs.session import Session

        log.debug('Get spark session')

        Session(spark_session=spark)
        if Config().file_system_type == FileSystemType.blob:
            spark.conf.set(
                f'fs.azure.account.key.{Config().file_system.staging_props.get("storage_account_name")}.'
                f'blob.core.windows.net',
                Config().file_system.staging_props.get('storage_account_key')
            )

from osci.actions import Action
from osci.actions.process import (
    DailyOSCIRankingsAction,
    CompanyContributorsRankingAction,
    CompanyContributorsReposRankingAction,
    CompanyMonthByMonthCommitsAmountAction,
    CompanyReposRankingAction,
    DailyCompanyRankingsAction,
    OSCICommitsRankingAction,
    OSCIContributorsRankingAction,
    OSCILanguagesAction,
    OSCILicensesAction,
    OSCIRankingAction,
)


def get_actions_commands():
    """Find all available cli actions"""
    command_group = click.Group()

    for action in Action.__subclasses__():
        options = [
            click.Option([f'--{param.name}', f'-{param.short_name}'] if param.short_name else [f'--{param.name}'],
                         type=param.type if param.type != datetime else str,
                         required=param.required,
                         help=f"{param.description} "
                              f"{param.datetime_format if param.datetime_format else param.choices if param.choices else ''}",
                         default=param.default)
            for param in action.params
        ]
        try:
            command = click.Command(name=action.name(), params=options, callback=action().execute,
                                    short_help=action.__doc__, help=action.help_text())
            command_group.add_command(command)
        except NotImplementedError as ex:
            log.warning(f'Action `{action}` skipped; ex: {ex}')
            continue
    return command_group


cli = click.CommandCollection(sources=[
    get_actions_commands(),
])

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
    cli(standalone_mode=False)
