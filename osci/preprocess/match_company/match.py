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

from typing import Optional
from .company_domain_matcher import CompanyDomainMatcher

import re

EMAIL_REGEXP = r'^[a-zA-Z0-9_.+-]+@(?P<domain>[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$'


def match_company_by_email(email: str) -> Optional[str]:
    email_match = re.match(EMAIL_REGEXP, email)
    if email_match:
        return CompanyDomainMatcher().match_company_by_domain(domain=email_match.group('domain'))
    return


if __name__ == '__main__':
    cli()
