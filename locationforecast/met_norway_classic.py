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
from typing import Union, List

from forecast import ForecastEntry
from .constants import (
    NAME_ATTRIB,
    DEG_ATTRIB, MPS_ATTRIB, BEAUFORT_ATTRIB, NUM_ATTRIB, ID_ATTRIB,
    TEMPERATURE_TAG, WIND_DIRECTION_TAG, WIND_SPEED_TAG,
    WIND_GUST_TAG, HUMIDITY_TAG, PRECIPITATION_TAG, SYMBOL_TAG
)
from .provider import (
    LocationforecastProvider, ForecastAttrib, DFLT_TEMP_UNIT, DLFT_PERCENT_UNIT,
    DLFT_SPEED_UNIT, DLFT_HEIGHT_UNIT, DLFT_DEG_UNIT
)

# Met Norway forecast attributes
MN_ATTRIBUTES = {
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
        # Met Norway doesn't provide precipitation probability in
        # locationforecast classic ver 2.0
    ],
    SYMBOL_TAG: [
        ForecastAttrib.of_no_unit(ForecastEntry.SYMBOL_KEY, NUM_ATTRIB),
        ForecastAttrib.of_no_unit(ForecastEntry.ALT_TEXT_KEY, ID_ATTRIB),
    ]
}


class MetNorwayClassicProvider(LocationforecastProvider):
    """
    Forecast provider
    """

    def __init__(self, name: str, friendly_name: str, url: str, data_url: str,
                 lat_q: str, lng_q: str, tz: str,
                 country: Union[str, List[str]]):
        """
        Constructor

        :param name: Name of provider
        :param friendly_name: User friendly name of provider
        :param url: URL of provider
        :param data_url: data URL of provider
        :param lat_q: Latitude query parameter
        :param lng_q: Longitude query parameter
        :param tz: Timezone identifier of provider
        :param country: ISO 3166-1 alpha-2 country code of provider
        """
        super().__init__(
            name, friendly_name, url, data_url, lat_q, lng_q, tz, country,
            MN_ATTRIBUTES)
