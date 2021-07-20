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
from pathlib import Path
import yaml

from osci.utils import MetaSingleton

DEFAULT_BLACKLIST_PATH = Path(__file__).parent.resolve() / 'blacklist.yml'


class Blacklist(metaclass=MetaSingleton):
    def __init__(self, path=DEFAULT_BLACKLIST_PATH):
        self.path = path
        self.blocked_accounts = frozenset()
        self._load_file()

    def _load_file(self):
        blocked_accounts = []
        with open(self.path) as f:
            black_list = yaml.load(f, Loader=yaml.FullLoader) or []
            for blocked in black_list:
                if 'github_account' in blocked:
                    blocked_accounts.append(blocked['github_account'])
        self.blocked_accounts = frozenset(blocked_accounts)

    def is_blocked_account(self, account_name: str) -> bool:
        return account_name in self.blocked_accounts

    def is_blocked_repo_by_account(self, repository_name: str) -> bool:
        return self.is_blocked_account(account_name=repository_name.split('/')[:1][0])
