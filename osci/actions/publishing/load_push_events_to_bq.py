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
from osci.actions import Action, ActionParam
from typing import Dict, Any
from osci.publishing import load_push_events_to_bq
import datetime


class LoadPushEventTOBQAction(Action):
    params = Action.params + (
        ActionParam(name='hour', short_name='h', type=int, required=False, default='0'),
    )

    @classmethod
    def name(cls) -> str:
        return "load-push-events-to-bq"

    def _execute(self, day: datetime.datetime, hour: int) -> Dict[str, Dict[str, Any]]:
        return load_push_events_to_bq(day, hour)
