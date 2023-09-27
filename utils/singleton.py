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
from typing import TypeVar, Any
from collections.abc import Callable

T = TypeVar("T")


class SingletonMixin:
    """
    Provides a singleton implementation
    """

    _instance: T

    @staticmethod
    def get_class_instance(cls: type, attrib_name: str, func: Callable = None) -> Any:
        """
        Get the instance

        :param cls: class of instance to get
        :param attrib_name: name of instance attribute
        :param func: constructor function; default None
        :return: instance
        """
        if not hasattr(cls, attrib_name):
            instance = func() if func else cls()
            setattr(cls, attrib_name, instance)
        else:
            instance = getattr(cls, attrib_name)
        return instance

    @classmethod
    def get_instance(cls) -> T:
        """
        Get the instance

        :return: instance
        """
        return cls.get_class_instance(cls, '_instance')
