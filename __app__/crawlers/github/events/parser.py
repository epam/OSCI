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

from typing import Dict, Type, Iterable, Iterator

from .base import Event
from .push import PushEvent, PushEventCommit

EVENT_TYPES: Dict[str, Type[Event]] = {
    "PushEvent": PushEvent
}


def parse_event(json_payload: dict) -> Event:
    return EVENT_TYPES.get(json_payload.get('type'), Event)(json_payload=json_payload)


def parse_events(payloads: Iterable[dict]) -> Iterator[Event]:
    yield from (parse_event(json_payload=payload) for payload in payloads)


def get_push_events(events: Iterable[Event]) -> Iterator[PushEvent]:
    yield from filter(lambda event: isinstance(event, PushEvent), events)


def get_push_events_commits(push_events: Iterable[PushEvent]) -> Iterator[PushEventCommit]:
    for push_event in push_events:
        yield from push_event.get_commits()
