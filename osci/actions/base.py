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
from typing import Type, NamedTuple, Optional, Dict, Union, Tuple, FrozenSet
from .exceptions import NotSuchParameterException, MissedRequiredParameterException
from osci.actions.consts import DAY_FORMAT, get_default_day
from datetime import datetime

import logging

log = logging.getLogger(__name__)


class ActionParam(NamedTuple):
    """Params for using in Action"""
    name: str
    short_name: Optional[str]
    type: Union[Type, Tuple[Type]] = str
    required: bool = False
    description: Optional[str] = ''
    datetime_format: Optional[str] = None
    default: Optional[str] = None
    choices: Optional[FrozenSet[str]] = None


class Action:
    """Check and validate command before execute commands"""
    params = (
        ActionParam(name='day', type=datetime, required=True, short_name='d'),
    )

    @classmethod
    def help_text(cls) -> str:
        """help text for cli click command"""
        return ''

    @classmethod
    def name(cls) -> str:
        """Name of the action"""
        raise NotImplementedError()

    def execute(self, **kwargs):
        """Process params and run _execute"""
        log.info(f'Execute action `{self.name()}`')
        log.info(f'Action params `{kwargs}`')
        return self._execute(**self._process_params(kwargs))

    def _execute(self, **kwargs):
        """Action process logic. Need to implement in subclasses"""
        raise NotImplementedError()

    @property
    def required_params(self) -> Dict[str, ActionParam]:
        return {param.name: param for param in self.params if param.required}

    @property
    def param_map(self) -> Dict[str, ActionParam]:
        return {param.name: param for param in self.params}

    @property
    def default_params(self) -> Dict[str, ActionParam]:
        return {param.name: param for param in self.params if param.default}

    def _set_default_params(self, processed_params: dict):
        """Set default params for not required params"""
        not_set_params = self.default_params.keys() - processed_params.keys()
        if not_set_params:
            for key in not_set_params:
                processed_params[key] = self.param_map[key].default

    def _check_required_params(self, passed: dict):
        missed_required = self.required_params.keys() - passed.keys() - self.default_params.keys()
        if missed_required:
            raise MissedRequiredParameterException('; '.join(missed_required))

    def _intersect_required_and_default_params(self):
        """Check intersection of required and default params"""
        common_param = set(self.required_params.keys()) & set(self.default_params.keys())
        if common_param:
            raise AttributeError(f"Parameter {common_param} "
                                 f"must be only `required` or `default`, not both")

    def _check_unknown_params(self, passed: dict):
        unknown = passed.keys() - self.param_map.keys()
        if unknown:
            raise NotSuchParameterException('; '.join(unknown))

    def _check_types(self, passed: dict):
        for k, v in passed.items():
            param = self.param_map[k]
            if param.type == datetime and isinstance(v, str):
                datetime.strptime(v, param.datetime_format or DAY_FORMAT)
                continue
            if param.type == int and isinstance(v, str):
                int(v)
                continue
            if not isinstance(v, param.type):
                raise TypeError(f'Param `{k}` type must be: `{param.type}` not `{type(v)}` (passed value: `{v}`)')
            if param.choices and (v not in param.choices):
                raise AttributeError(f"Param `{k}` must have values: {param.choices}")

    def _validate_params(self, passed: dict):
        self._check_required_params(passed)
        self._check_unknown_params(passed)
        self._check_types(passed)

    def _process_params(self, passed: dict):
        self._intersect_required_and_default_params()
        processed_params = passed.copy()
        self._set_default_params(processed_params)
        self._validate_params(passed)

        for param in self.params:
            if param.type == datetime and param.name in processed_params:
                processed_params[param.name] = datetime.strptime(processed_params[param.name],
                                                                 param.datetime_format or DAY_FORMAT)
            elif param.type == int and param.name in processed_params:
                processed_params[param.name] = int(processed_params[param.name])

        return processed_params
