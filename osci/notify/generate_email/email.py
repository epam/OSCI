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
import pandas as pd

from pathlib import Path
from jinja2 import Template
from datetime import datetime

log = logging.getLogger(__name__)

DEFAULT_TEMPLATE_PATH = Path(__file__).parent.resolve() / 'email.template.html'


class EmailBodyTemplate:
    def __init__(self, template_path: Path = DEFAULT_TEMPLATE_PATH):
        self.template = self.__load_template(path=template_path)

    @staticmethod
    def __load_template(path: Path):
        log.debug(f'Read template from {path}')
        with open(str(path)) as template_file:
            return Template(template_file.read())

    def render(self,
               date: datetime,
               compared_date: datetime,
               shift_up: pd.DataFrame,
               shift_down: pd.DataFrame,
               company: str,
               company_position: pd.DataFrame,
               solutionshub_osci_change_ranking: str,
               osci_reports_urls: dict
               ) -> str:
        return self.template.render(
            date=date,
            compared_date=compared_date,
            shift_up=shift_up.to_html(index=False),
            shift_down=shift_down.to_html(index=False),
            company=company,
            company_position=company_position.to_html(index=False),
            solutionshub_osci_change_ranking=solutionshub_osci_change_ranking,
            **osci_reports_urls
        )
