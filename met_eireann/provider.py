"""
Met Eireann forecast provider
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
from forecast import Provider


class MetEireannProvider(Provider):
    """
    Forecast provider
    """
    lat_q: str      # Latitude query parameter
    long_q: str     # Longitude query parameter
    from_q: str     # From date/time query parameter
    to_q: str       # To date/time query parameter

    def __init__(self, name: str, url: str, lat_q: str, long_q: str,
                 from_q: str, to_q: str):
        """
        Constructor

        :param name: Name of provider
        :param url: URL of provider
        :param lat_q: Latitude query parameter
        :param long_q: Longitude query parameter
        :param from_q: From date/time query parameter
        :param to_q: To date/time query parameter
        """
        super().__init__(name, url)
        self.lat_q = lat_q
        self.long_q = long_q
        self.from_q = from_q
        self.to_q = to_q

    def location_url(self, latitude: str, longitude: str, **kwargs) -> str:
        """
        Get forecast url for a location

        :param latitude: Latitude of the location
        :param longitude: Longitude of the location
        :return: url
        """
        return f"{self.url}?{self.lat_q}={latitude}&{self.long_q}={longitude}"

    def get_forecast(self, location: str, **kwargs) -> dict:
        pass

    def __str__(self):
        return f"{self.name}, {self.url}"
