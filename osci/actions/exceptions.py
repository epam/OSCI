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


class ActionException(Exception):
    """An exception that Action can handle and show to the user."""

    exit_code = 1

    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message

    def format_message(self):
        return self.message

    def __str__(self):
        return self.format_message()


class NotSuchParameterException(ActionException):
    def format_message(self):
        return f'Not such parameter `{self.message}`'


class MissedRequiredParameterException(ActionException):
    def format_message(self):
        return f'Missed required: {self.message}'
