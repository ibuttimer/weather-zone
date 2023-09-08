#  MIT License
#
#  Copyright (c) 2023 Ian Buttimer
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
import sys
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Any, Callable, Optional, Type, Union, List

from .misc import ensure_list, is_boolean_true

TypeChoiceArg = TypeVar("TypeChoiceArg", bound="ChoiceArg")
TypeQueryStatus = TypeVar("TypeQueryStatus", bound="QueryStatus")
TypeQueryArg = TypeVar("TypeQueryArg", bound="QueryArg")
TypeQueryOption = TypeVar("TypeQueryOption", bound="QueryOption")


class ChoiceArg(Enum):
    """ Enum representing options with limited choices """
    display: str
    """ Display string """
    arg: Any
    """ Argument value """

    def __init__(self, display: str, arg: Any):
        self.display = display
        self.arg = arg

    @staticmethod
    def _lower_str(val):
        """ Lower string value function for filtering """
        return val.lower() if isinstance(val, str) else val

    @staticmethod
    def _pass_thru(val):
        """ Pass-through filter function """
        return val

    @classmethod
    def _find_value(
            cls, arg: Any, func: Callable = None) -> Optional[TypeChoiceArg]:
        """
        Get value matching specified `arg`
        :param arg: arg to find
        :param func: value transform function to be applied before comparison;
                     default pass-through
        :return: ChoiceArg value or None if not found or multiple matches
        """
        if func is None:
            func = cls._pass_thru

        matches = list(
            filter(
                lambda val: func(val) == arg,
                cls
            )
        )
        return matches[0] if len(matches) == 1 else None

    @classmethod
    def from_arg(
            cls, arg: Any, func: Callable = None) -> Optional[TypeChoiceArg]:
        """
        Get value matching specified `arg`
        :param arg: arg to find
        :param func: value transform function to be applied before comparison;
                     default convert to lower-case string
        :return: ChoiceArg value or None if not found or multiple matches
        """
        if func is None:
            def trans_func(val):
                return cls._lower_str(val.arg)
            func = trans_func

        return cls._find_value(arg, func=func)

    @classmethod
    def from_display(
            cls, display: str, func: Callable = None
    ) -> Optional[TypeChoiceArg]:
        """
        Get value matching specified display string
        :param display: display string to find
        :param func: value transform function to be applied before comparison;
                     default convert to lower-case string
        :return: ChoiceArg value or None if not found
        """
        if func is None:
            def trans_func(val):
                return cls._lower_str(val.display)
            func = trans_func
            display_func = cls._lower_str
        else:
            display_func = cls._pass_thru

        return cls._find_value(display_func(display), func=func)

    @staticmethod
    def arg_if_choice_arg(obj):
        """
        Get the value if `obj` is a ChoiceArg, otherwise `obj`
        :param obj: object to get value of
        :return: value
        """
        return obj.arg \
            if isinstance(obj, ChoiceArg) else obj


class QueryArg:
    """ Class representing http request query args """
    value: Any
    """ Value """
    was_set: bool
    """ Argument was set in request flag """

    def __init__(self, value: Any, was_set: bool):
        self.set(value, was_set)

    def set(self, value: Any, was_set: bool):
        """
        Set the value and flags
        :param value: value to set
        :param was_set: set in request flag
        :return:
        """
        self.value = value
        self.was_set = was_set

    def was_set_to_one_of(self, values: List[Any], attrib: str = None):
        """
        Check if value was set to one of the specified `values`
        :param values: values to check
        :param attrib: attribute of set value to check; default None
        :return: True if value was set to one of the specified values
        """
        chk_value = self.value if not attrib else getattr(self.value, attrib)
        return self.was_set and chk_value in values

    def was_set_to(self, value: Any, attrib: str = None):
        """
        Check if value was set to the specified `value`;
        'true', 'on', 'ok', 'y', 'yes', '1'
        :param value: value to check
        :param attrib: attribute of set value to check; default None
        :return: True if value was set to the specified `value`
        """
        return self.was_set_to_one_of(ensure_list(value), attrib=attrib)

    def was_set_to_boolean_true(self, attrib: str = None):
        """
        Check if value was set to a boolean true value
        :param attrib: attribute of set value to check; default None
        :return: True if value was set to boolean true
        """
        chk_value = self.value if not attrib else getattr(self.value, attrib)
        return is_boolean_true(str(chk_value))

    @property
    def as_tuple(self) -> tuple[Any, bool]:
        """
        Return this object as a tuple of its properties
        :return: tuple of value, was_set
        """
        return self.value, self.was_set

    @property
    def value_arg_or_value(self) -> Any:
        """
        Get the arg value if this object's value is a ChoiceArg, otherwise
        this object's value
        :return: value
        """
        return self.value.arg \
            if isinstance(self.value, ChoiceArg) else self.value

    @staticmethod
    def value_arg_or_object(obj) -> Any:
        """
        Get the arg value if `obj` is a ChoiceArg, otherwise `obj`
        :param obj: object to get value of
        :return: value
        """
        return ChoiceArg.arg_if_choice_arg(obj.value) \
            if isinstance(obj, QueryArg) else obj

    @staticmethod
    def of(obj) -> TypeQueryArg:
        """
        Get an unset QueryArg with the value 0f `obj`
        :param obj: value
        :return: new QueryArg
        """
        return QueryArg(obj, False)

    def __str__(self):
        return f'{self.value}: was_set {self.was_set}'


QueryArg.NONE = QueryArg.of(None)


@dataclass
class QueryOption:
    """
    Request query option class
    """
    query: str
    """ Query key """
    clazz: Optional[Type[ChoiceArg]]
    """ Class of choice result """
    default: Union[ChoiceArg, Any]
    """ Default choice """

    @classmethod
    def of_no_cls_dflt(
            cls: Type[TypeQueryOption], query: str) -> TypeQueryOption:
        """ Get QueryOption with no class or default """
        return cls(query=query, clazz=None, default=None)

    @classmethod
    def of_no_cls(
        cls: Type[TypeQueryOption], query: str, default: Union[ChoiceArg, Any]
    ) -> TypeQueryOption:
        """ Get QueryOption with no class or default """
        return cls(query=query, clazz=None, default=default)


class SortOrder(ChoiceArg):
    """ Base enum representing sort orders """

    def __init__(self, display: str, arg: str, order: str):
        super().__init__(display, arg)
        self.order = order


class PerPageMixin:
    """ Mixin for enums representing items per page """

    @staticmethod
    def all_value():
        """ Get the value representing all items """
        return sys.maxsize

    def __init__(self, count: int):
        self._all = count == self.all_value()

    @property
    def is_all(self):
        """ Is this enum representing all items """
        return self._all


class PerPage6(PerPageMixin, ChoiceArg):
    """ Enum representing items per page, initial 6/pg step 3 """
    SIX = 6
    NINE = 9
    TWELVE = 12
    FIFTEEN = 15

    def __init__(self, count: int):
        super().__init__(count)     # PerPageMixin __init__
        # self.__class__.__mro__ = (
        #   <enum 'PerPage6'>, <class 'utils.enums.PerPageMixin'>,
        #   <enum 'ChoiceArg'>, <enum 'Enum'>, <class 'object'>
        # ) so type for super is PerPageMixin to hit ChoiceArg
        super(PerPageMixin, self).__init__(f'{count} per page', count)


PerPage6.DEFAULT = PerPage6.SIX


class PerPage8(PerPageMixin, ChoiceArg):
    """ Enum representing items per page, initial 8/pg step 4 """
    EIGHT = 8
    TWELVE = 12
    SIXTEEN = 16
    TWENTY = 20

    def __init__(self, count: int):
        super().__init__(count)     # PerPageMixin __init__
        # ChoiceArg __init__, see PerPage6.__init__ comment
        super(PerPageMixin, self).__init__(f'{count} per page', count)


PerPage8.DEFAULT = PerPage8.EIGHT


class PerPage50(PerPageMixin, ChoiceArg):
    """ Enum representing items per page, initial 50/pg step 50 """
    FIFTY = 50
    ONE_HUNDRED = 100
    ONE_FIFTY = 150
    TWO_HUNDRED = 200
    TWO_FIFTY = 250
    ALL = PerPageMixin.all_value()

    def __init__(self, count: int):
        super().__init__(count)     # PerPageMixin __init__
        # ChoiceArg __init__, see PerPage6.__init__ comment
        super(PerPageMixin, self).__init__(
            f'{count} per page' if count != PerPageMixin.all_value() else
            'All', count)


PerPage50.DEFAULT = PerPage50.FIFTY


class YesNo(ChoiceArg):
    """ Enum representing a truthy choice """
    NO = ('No', 'no')
    YES = ('Yes', 'yes')
    IGNORE = ('Ignore', 'na')

    @property
    def boolean(self) -> Optional[bool]:
        """ Boolean representation of choice """
        return True if self == YesNo.YES else \
            False if self == YesNo.NO else None


YesNo.DEFAULT = YesNo.IGNORE
