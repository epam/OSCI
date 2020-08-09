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

from pathlib import Path
from typing import Optional

import yaml
import re

DEFAULT_MATCH_LIST_PATH = Path(__file__).parent.resolve() / 'company_domain_match_list.yaml'


class MetaSingleton(type):
    """Metaclass for create singleton"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CompanyDomainMatcher(metaclass=MetaSingleton):

    def __init__(self, path=DEFAULT_MATCH_LIST_PATH):
        self.path = path
        self._domain2company = dict()
        self._regex2company = dict()
        self._load_file()

    def _load_file(self):
        with open(self.path) as f:
            match_list = yaml.load(f, Loader=yaml.FullLoader) or []
            for company in match_list:
                name = company.get('company')
                for domain in company.get('domains') or []:
                    self._domain2company[domain] = name
                for regex in company.get('regex') or []:
                    self._regex2company[regex] = name

    def match_company_by_domain(self, domain: str) -> Optional[str]:
        company = self._domain2company.get(domain)
        if company is not None:
            return company
        for regex in self._regex2company.keys():
            if re.match(regex, domain):
                return self._regex2company[regex]
        return None

    @classmethod
    def tear_down(cls):
        """Delete all instances of the class"""
        cls._instances = {}
