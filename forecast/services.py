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
from socket import inet_aton
from typing import Optional

from django.http import HttpRequest
from django.conf import settings

from geoip2.webservice import Client as GeoIpClient
from geoip2.errors import AddressNotFoundError

from broker import IService

from utils import SingletonMixin

from .geocoding import geocode_address


class GeocodeService(SingletonMixin, IService):
    """
    Geocode service
    """


# add GeocodeService-specific methods to GeocodeService class
GeocodeService.geocode_address = IService.make_api_method(geocode_address)


class GeoIpService(SingletonMixin, IService):
    """
    GeoIP service
    """
    _geo_ip_client: GeoIpClient

    def _geo_ip_client_constructor(self) -> GeoIpClient:
        """
        GeoIP client constructor
        :return: GeoIP client
        """
        return GeoIpClient(
            settings.MAXMIND_GEOIP_ACCOUNT, settings.MAXMIND_GEOIP_KEY,
            host='geolite.info')


    def is_valid_ip(self, ip_string: str):
        is_valid = True
        try:
            inet_aton(ip_string)
        except OSError:
            is_valid = False
        return is_valid

    def get_request_country(self, request: HttpRequest) -> Optional[str]:
        """
        Get the country code from the request
        :param request: http request object
        :return: ISO 3166-1 alpha-2 country code
        """
        address, country = (None, None)

        # try to get the country code from the request
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if forwarded:
            # first IP from the leftmost that is a valid address (only IPv4)
            addresses = list(map(lambda x: x.strip(), forwarded.split(',')))
            addresses = list(filter(self.is_valid_ip, addresses))
            address = addresses[0] if addresses else None

        # TODO Forwarded header
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Forwarded

        if address is None:
            address = request.META.get('REMOTE_ADDR', None)
            if not self.is_valid_ip(address):
                address = None

        if address:
            client = self.get_class_instance(
                self.__class__, '_geo_ip_client',
                func=self._geo_ip_client_constructor)

            try:
                country = client.country(address)
            except AddressNotFoundError:
                country = None

        return country.country.iso_code if country else None
