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

from osci.datalake.schemas.public import OSCIChangeRankingSchema, OSCIGrowthSpeedSchema
from osci.datalake import DatePeriodType

from .base import Report


class OSCIChangeRanking(Report):
    base_name = 'OSCI_change_ranking'
    schema = OSCIChangeRankingSchema
    date_period = DatePeriodType.YTD

    @property
    def name(self) -> str:
        """Return the only base name"""
        return self.base_name


class OSCIChangeRankingDTD(Report):
    """Daily change report"""
    base_name = 'OSCI_Change_ranking'
    schema = OSCIChangeRankingSchema
    date_period = DatePeriodType.DTD


class OSCIGrowthSpeed(Report):
    base_name = 'OSCI_growth_speed'
    schema = OSCIGrowthSpeedSchema
