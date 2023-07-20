"""
Provides a registry of forecast providers
"""
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
from typing import TypeVar, Optional

from .iprovider import IProvider

TypeRegistry = TypeVar('TypeRegistry', bound='Registry')


class Registry:
    """
    Provides a registry of forecast providers
    """

    providers: dict

    _registry: TypeRegistry

    def __init__(self):
        self.providers = {}

    @staticmethod
    def get_registry() -> TypeRegistry:
        """
        Get the registry

        :return: Registry
        """
        if not hasattr(Registry, '_registry'):
            Registry._registry = Registry()
        return Registry._registry

    def is_registered(self, name: str) -> bool:
        """
        Is a provider registered

        :param name: Name of provider
        :return: True if registered, otherwise False
        """
        return name in self.providers

    def add(self, name: str, provider: IProvider,
            raise_on_reg: bool = True) -> bool:
        """
        Add a provider to the registry

        :param name: Name of provider
        :param provider: Provider to add
        :param raise_on_reg: raise an exception if already registered;
                            default True
        :return: True if added, otherwise False
        """
        registered = self.is_registered(name)
        if registered and raise_on_reg:
            raise ValueError(f"Provider '{name}' already registered")
        if not registered:
            self.providers[name] = provider
            registered = True
        return registered

    def get(self, name: str, raise_not_reg: bool = True) -> Optional[IProvider]:
        """
        Get a provider from the registry

        :param name: Name of provider
        :param raise_not_reg: raise an exception if not registered;
                            default True
        :return: Provider
        """
        registered = self.is_registered(name)
        if not registered and raise_not_reg:
            raise ValueError(f"Provider '{name}' not registered")
        return self.providers[name] if registered else None
