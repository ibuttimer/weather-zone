"""
Forecast provider
"""
# MIT License
#
# Copyright (c) 2023 Ian Buttimer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from abc import ABC

from .iprovider import IProvider


class Provider(IProvider, ABC):
    """
    Forecast provider
    """
    name: str   # Name of provider
    url: str    # URL of provider

    def __init__(self, name: str, url: str):
        """
        Constructor

        :param name: Name of provider
        :param url: URL of provider
        """
        self.name = name
        self.url = url

    def __str__(self):
        return f"{self.name}, {self.url}"

    def get_name(self) -> str:
        """
        Get the name of the provider

        :return: Name of provider
        """
        return self.name

    def get_url(self) -> str:
        """
        Get the url of the provider

        :return: URL of provider
        """
        return self.url