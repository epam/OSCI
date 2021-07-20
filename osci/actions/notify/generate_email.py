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
from osci.actions import Action
from osci.notify.generate_email import generate_email_body

from datetime import datetime


class GenerateEmailAction(Action):
    """Generate report for sending via email"""

    @classmethod
    def help_text(cls) -> str:
        return "prepare OSCI change ranking report to the email format"

    @classmethod
    def name(cls):
        return 'generate-email'

    def _execute(self, day: datetime):
        return generate_email_body(date=day)
