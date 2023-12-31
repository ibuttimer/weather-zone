"""
Constants for forecast app
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
from pathlib import Path

from utils import append_slash, url_path

# name of this app
THIS_APP = Path(__file__).resolve().parent.name

PK_PARAM_NAME = "pk"

# routes related
ADDRESS_URL = append_slash("address")
LAT_LONG_URL = append_slash("geo-coordinate")
DISPLAY_URL = url_path("display")
DISPLAY_ADDRESS_URL = url_path(DISPLAY_URL, "address",
                               f"<int:{PK_PARAM_NAME}>")
DASH_URL = url_path("dash")

ADDRESS_ROUTE_NAME = "address"
LAT_LONG_ROUTE_NAME = "geo-coordinate"
DISPLAY_ROUTE_NAME = "display"
DISPLAY_ADDRESS_ROUTE_NAME = "display-address"
DASH_ROUTE_NAME = "dash"

QUERY_PARAM_LAT = "lat"
QUERY_PARAM_LONG = "lng"
QUERY_PARAM_FROM = "from"
QUERY_PARAM_TO = "to"
QUERY_TIME_RANGE = "time_rng"
QUERY_PROVIDER = "provider"

# context variables
FORECAST_MENU_CTX = "forecast_menu"

ADDRESS_FORM_CTX = "address_form"
UNAUTH_SKIP_FIELDS_CTX = "unauth_skip_fields"
SUBMIT_URL_CTX = "submit_url"
EMBED_MAP_CTX = "embed_map"
FORECAST_LIST_CTX = "forecast_list"
FORECAST_CTX = "forecast"
ROW_TYPES_CTX = "row_types"
WARNING_LIST_CTX = "warning_list"
WARNING_CTX = "warning"
WARNING_URL_CTX = "warning_url"
WARNING_URL_ARIA_CTX = "warning_url_aria"
SUBMIT_BTN_TEXT_CTX = 'submit_btn_text'

# provider selection
ALL_PROVIDERS = 'all'
COUNTRY_PROVIDERS = 'country'

# service-specific
GEOCODE_SERVICE = 'GeocodeService'
GEOCODE_ADDRESS_FUNC = 'geocode_address'
GEOIP_SERVICE = 'GeoIpService'
GET_REQUEST_COUNTRY_FUNC = 'get_request_country'

# field names of GeoCodeResult
COMPONENTS_FIELD = 'components'
COUNTRY_FIELD = 'country'
FORMATTED_ADDR_FIELD = 'formatted_addr'
LATITUDE_FIELD = 'latitude'
LONGITUDE_FIELD = 'longitude'
PLACE_ID_FIELD = 'place_id'
GLOBAL_PLUS_CODE_FIELD = 'global_plus_code'
COMPOUND_PLUS_CODE_FIELD = 'compound_plus_code'
RES_TYPE_FIELD = 'res_type'
