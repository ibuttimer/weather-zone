"""
Locationforecast forecast provider
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
from typing import Dict, Tuple, Union, List

from forecast import ForecastEntry
from .constants import (
    NAME_ATTRIB,
    DEG_ATTRIB, MPS_ATTRIB, BEAUFORT_ATTRIB, PERCENT_LITERAL,
    PROBABILITY_ATTRIB, NUM_ATTRIB, ID_ATTRIB, OLD_ID_PROP,
    VARIANTS_PROP, TEMPERATURE_TAG, WIND_DIRECTION_TAG, WIND_SPEED_TAG,
    WIND_GUST_TAG, HUMIDITY_TAG, PRECIPITATION_TAG, SYMBOL_TAG
)
from .provider import (
    LocationforecastProvider, ForecastAttrib, NO_LEGEND_ADDENDUM,
    DAY_LEGEND_ADDENDUM, NIGHT_LEGEND_ADDENDUM,
    DFLT_TEMP_UNIT, DLFT_PERCENT_UNIT, DLFT_SPEED_UNIT, DLFT_HEIGHT_UNIT,
    DLFT_DEG_UNIT
)

DARK_LEGEND_OFFSET = 100    # offset of dark variant legends

# Met Eireann forecast attributes
ME_ATTRIBUTES = {
    TEMPERATURE_TAG: ForecastAttrib.of_unit_val(
        ForecastEntry.TEMPERATURE_KEY, DFLT_TEMP_UNIT),
    WIND_DIRECTION_TAG: [
        ForecastAttrib.of_attrib_unit(
            ForecastEntry.WIND_DIR_KEY, DEG_ATTRIB, DLFT_DEG_UNIT),
        ForecastAttrib.of_no_unit(
            ForecastEntry.WIND_CARDINAL_KEY, NAME_ATTRIB)
    ],
    WIND_SPEED_TAG: [
        ForecastAttrib.of_attrib_unit(
            ForecastEntry.WIND_SPEED_KEY, MPS_ATTRIB, DLFT_SPEED_UNIT),
        ForecastAttrib.of_no_unit(
            ForecastEntry.BEAUFORT_KEY, BEAUFORT_ATTRIB),
    ],
    WIND_GUST_TAG: ForecastAttrib.of_attrib_unit(
        ForecastEntry.WIND_GUST_KEY, MPS_ATTRIB, DLFT_SPEED_UNIT),
    HUMIDITY_TAG: ForecastAttrib.of_unit_val(
        ForecastEntry.HUMIDITY_KEY, DLFT_PERCENT_UNIT),
    PRECIPITATION_TAG: [
        ForecastAttrib.of_unit_val(
            ForecastEntry.PRECIPITATION_KEY, DLFT_HEIGHT_UNIT),
        ForecastAttrib(
            ForecastEntry.PRECIPITATION_PROB_KEY, PERCENT_LITERAL,
            PROBABILITY_ATTRIB, DLFT_PERCENT_UNIT)
    ],
    SYMBOL_TAG: [
        ForecastAttrib.of_no_unit(ForecastEntry.SYMBOL_KEY, NUM_ATTRIB),
        ForecastAttrib.of_no_unit(ForecastEntry.ALT_TEXT_KEY, ID_ATTRIB),
    ]
}


class MetEireannForecastProvider(LocationforecastProvider):
    """
    Met Éireann forecast provider
    """
    FROM_PROP = 'from_q'
    TO_PROP = 'to_q'

    from_q: str     # From date/time query parameter
    to_q: str       # To date/time query parameter

    def __init__(self, name: str, friendly_name: str, url: str,
                 lat_q: str, lng_q: str, from_q: str, to_q: str,
                 tz: str, country: Union[str, List[str]]):
        """
        Constructor

        :param name: Name of provider
        :param friendly_name: User friendly name of provider
        :param url: URL of provider
        :param lat_q: Latitude query parameter
        :param lng_q: Longitude query parameter
        :param from_q: From date/time query parameter
        :param to_q: To date/time query parameter
        :param tz: Timezone identifier of provider
        :param country: ISO 3166-1 alpha-2 country code of provider
        """
        super().__init__(
            name, friendly_name, url, lat_q, lng_q, tz, country, ME_ATTRIBUTES)
        self.from_q = from_q
        self.to_q = to_q

    def url_params(self, lat: float, lng: float, start: datetime = None,
                   end: datetime = None, **kwargs) -> dict:
        """
        Get query params of forecast url for a location

        :param lat: Latitude of the location
        :param lng: Longitude of the location
        :param start: forecast start date; default is current time
        :param end: forecast end date; default is end of available forecast
        :return: url
        """
        # https://data.gov.ie/dataset/met-eireann-weather-forecast-api
        # http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast?lat=<LATITUDE>;long=<LONGITUDE>;from=2018-11-10T02:00;to=2018-11-12T12:00
        params = super().url_params(lat, lng)
        for q, v in [(self.from_q, start), (self.to_q, end)]:
            if v is not None:
                params[q] = v.strftime('%Y-%m-%dT%H:%M')
        return params

    def get_id_variant(self, legend: Dict) -> Tuple[int, str]:
        """
        Get the id and variant addendum for icon filename
        :param legend: legend to get id and variant from
        :return: tuple of id and variant addendum
        """
        addendum = DAY_LEGEND_ADDENDUM if legend.get(VARIANTS_PROP, None) \
            else NO_LEGEND_ADDENDUM
        old_id = int(legend.get(OLD_ID_PROP))
        if old_id > DARK_LEGEND_OFFSET:
            old_id -= DARK_LEGEND_OFFSET
            assert old_id > 0
            addendum = NIGHT_LEGEND_ADDENDUM
        return old_id, addendum
