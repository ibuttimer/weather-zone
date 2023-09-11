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
from datetime import datetime
from typing import TypeVar, Optional, List, Callable

from broker import Broker, ServiceType
from utils import SingletonMixin, ensure_list

from .dto import Forecast, GeoAddress, WeatherWarnings
from .iprovider import IProvider
from .constants import COUNTRY_PROVIDERS

TypeRegistry = TypeVar('TypeRegistry', bound='Registry')


class Registry(SingletonMixin):
    """
    Provides a singleton registry of forecast providers
    """

    _broker: Broker

    def __init__(self):
        self._broker = Broker.get_instance()

    def is_registered(self, name: str) -> bool:
        """
        Is a provider registered

        :param name: Name of provider
        :return: True if registered, otherwise False
        """
        return self._broker.is_registered(
            name, *ServiceType.weather_types())

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
            self._broker.add(name, provider.stype, provider)
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
        return self._broker.get(name, ServiceType.weather_types(),
                                raise_not_reg=raise_not_reg)

    def provider_names(self, stype: ServiceType = None,
                       filter_func: Callable = None) -> List[str]:
        """
        Get the provider names

        :param stype: Provider type to filter on; default None
        :param filter_func: Filter function to apply to providers; default None
        :return: Provider names
        """
        return self._broker.provider_names(
            service_type=ServiceType.weather_types() if stype is None
            else ensure_list(stype),
            filter_func=filter_func
        )

    @property
    def providers(self) -> List[IProvider]:
        """
        Get the providers

        :return: Providers
        """
        return self._broker.providers(
            ServiceType.weather_types() if self.stype is None else
            ensure_list(self.stype)
        )

    def generate_forecast(
            self, geo_address: GeoAddress, start: datetime = None,
            end: datetime = None, provider: str = None,
            **kwargs) -> List[Forecast]:
        """
        Get a list of forecasts
        :param geo_address: geographic address
        :param start: forecast start date; default is current time
        :param end: forecast end date; default is end of available forecast
        :param provider: name of forecast provider; default is all providers
        :param kwargs: Additional arguments
        :return: Forecast
        """
        forecasts = []

        def is_supported(prov: IProvider) -> bool:
            return prov.is_country_supported(geo_address.country)

        if provider and provider.lower() == COUNTRY_PROVIDERS:
            filter_func = is_supported
            provider = None
        else:
            filter_func = is_supported

        providers = [provider] if provider is not None \
            else self.provider_names(stype=ServiceType.FORECAST,
                                     filter_func=filter_func)

        for name in providers:
            forecasts.append(
                self.get(name).get_geo_forecast(
                    geo_address, start, end, **kwargs)
            )

        return forecasts

    def generate_warnings(self, country: str, provider_name: str = None,
                          **kwargs) -> List[WeatherWarnings]:
        """
        Get a list of weather warnings
        :param country: ISO 3166-1 alpha-2 country code
        :param provider_name: name of forecast provider; default is all providers
        :param kwargs: Additional arguments
        :return: list of weather warnings
        """
        warnings = []
        providers = self.provider_names(stype=ServiceType.WARNING)
        if provider_name is not None and provider_name in providers:
            providers = [provider_name]

        for name in providers:
            provider = self.get(name)
            # filter providers by country
            if provider.is_country_supported(country):
                warnings.append(
                    provider.get_warnings(**kwargs)
                )

        return warnings

    def generate_warnings_summary(self, country: str, provider: str = None,
                                  **kwargs) -> List[WeatherWarnings]:
        """
        Get a summary of weather warnings
        :param country: ISO 3166-1 alpha-2 country code
        :param provider: name of forecast provider; default is all providers
        :param kwargs: Additional arguments
        :return: list of weather warnings
        """
        # TODO generate_warnings_summary for forecast page header
        return []
