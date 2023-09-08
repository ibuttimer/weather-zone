#  MIT License
#
#  Copyright (c) 2023 Ian Buttimer
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
import functools
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, List


class ServiceType(Enum):
    """
    Forecast provider types
    """
    UNKNOWN = auto()

    FORECAST = auto()   # forecast provider
    WARNING = auto()    # warning provider
    FORECAST_WARNING = auto()   # forecast and warning provider

    SERVICE = auto()    # basic service; IService
    DB_CRUD = auto()    # database CRUD service; ICrudService

    @classmethod
    def forecast_types(cls) -> List['ServiceType']:
        """
        Return a list of weather forecast types
        :return: list of weather forecast types
        """
        return [ServiceType.FORECAST, ServiceType.FORECAST_WARNING]

    @classmethod
    def warning_types(cls) -> List['ServiceType']:
        """
        Return a list of weather warning types
        :return: list of weather warning types
        """
        return [ServiceType.WARNING, ServiceType.FORECAST_WARNING]

    @classmethod
    def weather_types(cls) -> List['ServiceType']:
        """
        Return a list of weather service types
        :return: list of weather service types
        """
        return list(dict.fromkeys(cls.forecast_types() + cls.warning_types()))


class IService(ABC):
    """
    Interface for service classes
    """

    @staticmethod
    def make_api_method(func):
        """
        Provides a method of calling a function with the first argument removed,
        i.e. the self argument.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args[1:], **kwargs)
            return result
        return wrapper

    def execute(self, func: str, *args, **kwargs) -> Any:
        """
        Execute a function in the service
        :param func: function name
        :param args: arguments
        :param kwargs: keyword arguments
        :return:
        """
        if not hasattr(self, func):
            raise NotImplementedError(f'Unknown function {func}')
        # class instance is first argument, so if the function does not require
        # a reference to the class instance, use 'make_api_method' to wrap the
        # function and remove the first argument
        return getattr(self, func)(*args, **kwargs)


class ICrudService(IService):
    """
    Interface for service classes
    """

    @abstractmethod
    def create(self, *args, **kwargs) -> Any:
        """
        Perform the create action on the service
        :param args: arguments
        :param kwargs: keyword arguments
        :return:
        """

    @abstractmethod
    def get(self, *args, **kwargs) -> Any:
        """
        Perform the get action on the service
        :param args: arguments
        :param kwargs: keyword arguments
        :return:
        """

    @abstractmethod
    def update(self, *args, **kwargs) -> Any:
        """
        Perform the update action on the service
        :param args: arguments
        :param kwargs: keyword arguments
        :return:
        """

    @abstractmethod
    def delete(self, *args, **kwargs) -> Any:
        """
        Perform the delete action on the service
        :param args: arguments
        :param kwargs: keyword arguments
        :return:
        """
