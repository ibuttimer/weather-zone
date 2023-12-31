"""
Miscellaneous utility functions
"""
#  MIT License
#
#  Copyright (c) 2022-2023 Ian Buttimer
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#
from collections import namedtuple
from enum import Enum
from typing import List, Any, Callable, Optional, TypeVar, Dict

import environ

TypeCrud = TypeVar("TypeCrud", bound="Crud")


def is_boolean_true(text: str) -> bool:
    """
    Check if `text` represents a boolean True value;
    'true', 'on', 'ok', 'y', 'yes', '1'
    :param text: string to check
    :return: True if represents a boolean True value, otherwise False
    """
    return str(text).lower() in environ.Env.BOOLEAN_TRUE_STRINGS


class Crud(Enum):
    """
    Enum to map standard CRUD terms to Django models default permissions
    """
    # first term in tuple is django permission
    # second term in tuple is the REST method
    # and the rest are sensible alternative names
    CREATE = ('add', 'post', 'create', 'new')
    READ = ('view', 'get', 'read')
    UPDATE = ('change', 'put', 'update')
    DELETE = ('delete', 'remove')  # permission & method are the same

    @staticmethod
    def from_str(value: str) -> Optional[TypeCrud]:
        """
        Get enum object matching specified `string`
        :param value: string to match
        :return: Crud or None
        """
        crud = None
        value = value.lower()
        for action in Crud:
            if value in action.value:
                crud = action
                break
        return crud


def ensure_list(item: Any) -> List[Any]:
    """
    Ensure argument is returned as a list
    :param item: item(s) to return
    :return: list of item(s)
    """
    return item if isinstance(item, list) else [item]


def find_index(
        search: List[Any], sought: Any, start: int = None, end: int = None,
        mapper: Callable[[Any], Any] = None, replace: Any = None
) -> int:
    """
    Find the index of the first occurrence of `sought` in `search`
    (at or after index `start` and before index `end`)
    :param search: list to search
    :param sought: entry to search for
    :param start: index to begin search at; default start of `search`
    :param end: index to stop search before; default end of `search`
    :param mapper: func to map `search` entries before comparison;
                default None
    :param replace: value to replace entry with if found; default None
    :return: index of `sought`
    """
    if mapper is None:
        def pass_thru(entry):
            return entry

        mapper = pass_thru
    if start is None:
        start = 0
    if end is None:
        end = len(search)

    to_search = list(
        map(mapper, search)
    ) if mapper is not None else search

    index = to_search.index(sought, start, end)

    if index >= 0 and replace is not None:
        search[index] = replace

    return index


DictVal = namedtuple('DictVal', ['found', 'value'])


def dict_drill(obj: Dict, *args, default: Any = None,
               set_new: bool = False, new_value: Any = None) -> DictVal:
    """
    Drill into a dict object to retrieve a value
    :param obj: dict object
    :param args: attrib names
    :param default: default value to return if not found
    :param set_new: set new value, if True and found
    :param new_value: value to set
    :return: tuple of success flag and value
    """
    success = False
    last_idx = len(args) - 1
    value = obj
    for idx, key in enumerate(args):
        if key in value:
            if set_new and idx == last_idx:
                value[key] = new_value
            value = value[key]
        else:
            value = default
            break
    else:
        success = True
    return DictVal(success, value)


class AsDictMixin:
    """
    Mixin class to provide as_dict method
    """

    def as_dict(self, filter_fun: Callable = None) -> Dict[str, Any]:
        """
        Convert an object to a map
        :return: map
        """
        return {
            k: v for k, v in self.__dict__.items()
            if k not in object.__dict__ and not k.startswith('_')
            and not callable(v) and (filter_fun is None or filter_fun(k, v))
        }

    @staticmethod
    def filter_none_val(key: str, value: Any) -> bool:
        """
        Filter function to remove None values
        :param key: key
        :param value: value
        :return: True if value is not None, otherwise False
        """
        return value is not None
