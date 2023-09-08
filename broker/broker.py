"""
Provides a Broker of service providers
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
from re import sub
from typing import TypeVar, Optional, List, Dict, Union, Tuple, Callable

from utils import SingletonMixin, ensure_list
from .iservice import IService, ServiceType


TypeBroker = TypeVar('TypeBroker', bound='Broker')


class Broker(SingletonMixin):
    """
    Provides a singleton broker of service providers
    """

    _providers: Dict[ServiceType, Dict[str, IService]]

    def __init__(self):
        self._providers = {}

    def is_registered(self, name: str, *args) -> bool:
        """
        Is a provider registered

        :param name: Name of provider
        :param args: List of ServiceType to check; default all
        :return: True if registered, otherwise False
        """
        service_types = args if len(args) > 0 else tuple(ServiceType)

        for service_type in service_types:
            if service_type in self._providers and \
                    name in self._providers[service_type]:
                registered = True
                break
        else:
            registered = False
        return registered

    @staticmethod
    def is_valid_identifier(name: str) -> bool:
        """
        Check `name` is a valid identifier
        :param name:
        :return: True if valid, otherwise False
        """
        return name.isidentifier()

    def add(self, name: str, service_type: ServiceType, provider: IService,
            raise_on_reg: bool = True) -> bool:
        """
        Add a provider to the broker

        :param name: Name of provider
        :param service_type: Service type
        :param provider: Provider instance to add
        :param raise_on_reg: raise an exception if already registered;
                            default True
        :return: True if added, otherwise False
        """
        if not self.is_valid_identifier(name):
            raise ValueError(f"Service provider name '{name}' is invalid")
        registered = self.is_registered(name, service_type)
        if registered and raise_on_reg:
            raise ValueError(f"Service provider '{name}' already registered")
        if not registered:
            if service_type not in self._providers:
                self._providers[service_type] = {}

            self._providers[service_type][name] = provider
            registered = True

        return registered

    def _service_types(self,
                       service_type: Union[ServiceType, List, Tuple]
                       ) -> Tuple[ServiceType]:
        """
        Get the service types
        :param service_type: list, tuple or instance of ServiceType
        :return: tuple of Service type
        """
        return service_type if isinstance(service_type, tuple) else \
            tuple(service_type) if isinstance(service_type, list) else \
            (service_type,)

    def get(self, name: str, service_type: Union[ServiceType, List, Tuple],
            raise_not_reg: bool = True) -> Optional[IService]:
        """
        Get a provider from the Broker

        :param name: Name of provider
        :param service_type: list, tuple or instance of ServiceType
        :param raise_not_reg: raise an exception if not registered;
                            default True
        :return: Provider
        """
        for stype in self._service_types(service_type):
            if stype in self._providers and name in self._providers[stype]:
                provider = self._providers[stype][name]
                break
        else:
            provider = None

        if provider is None and raise_not_reg:
            raise ValueError(f"Provider '{name}' not registered")
        return provider

    def types_list(self, service_type: ServiceType = None) -> List[ServiceType]:
        """
        Get a ServiceType list

        :param service_type: Service type; default None
        :return: ServiceType list
        """
        return list(ServiceType) if service_type is None else \
            ServiceType.forecast_types() \
            if service_type == ServiceType.FORECAST else \
            ServiceType.weather_types() \
            if service_type == ServiceType.FORECAST_WARNING else \
            ensure_list(service_type)

    def provider_names(self, service_type: ServiceType = None,
                       filter_func: Callable = None) -> List[str]:
        """
        Get the provider names

        :param filter_func:
        :param service_type: Service type to filter on; default None
        :param filter_func: Filter function to apply to providers; default None
        :return: Provider names
        """
        if filter_func is None:
            def pass_thru(p: IService) -> bool:
                return True
            filter_func = pass_thru

        return [
            name for st, st_providers in self._providers.items()
            if st in self.types_list(service_type)
            for name, provider in st_providers.items()
            if filter_func(provider)
        ]

    def providers(self, service_type: ServiceType = None) -> List[IService]:
        """
        Get the providers

        :param service_type: Service type to filter on; default None
        :return: Providers
        """
        return [
            v for st, st_providers in self._providers.items()
            if st in self.types_list(service_type)
            for v in st_providers.values()
        ]


class ServiceCacheMixin:
    """
    Interface for cache service instances
    """

    def service(self, name: str,
                stype: ServiceType = ServiceType.SERVICE) -> IService:
        """
        Get a cached instance of a service
        :return: instance of service
        """
        # convert uppercase letters to '_<x>'
        ref_name = sub(r'([A-Z])', lambda m: f'_{m.group(1).lower()}', name)
        if not ref_name.startswith('_'):
            ref_name = f'_{ref_name}'
        if not Broker.is_valid_identifier(ref_name):
            raise ValueError(
                f"Unable to generate valid service provider name from '{name}'")

        if not hasattr(self, ref_name) or not getattr(self, ref_name):
            # save the service instance as an attribute
            setattr(self, ref_name, Broker.get_instance().get(name, stype))
        return getattr(self, ref_name)
