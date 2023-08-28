"""
User constants
"""
#  MIT License
#
#  Copyright (c) 2023 Ian Buttimer
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
from pathlib import Path

from utils import append_slash, url_path

# name of this app
THIS_APP = Path(__file__).resolve().parent.name

# field names of Address model
USER_FIELD = "user"
COUNTRY_FIELD = "country"
COMPONENTS_FIELD = "components"
FORMATTED_ADDR_FIELD = "formatted_addr"
LATITUDE_FIELD = "latitude"
LONGITUDE_FIELD = "longitude"
IS_DEFAULT_FIELD = "is_default"

# Address routes related
PK_PARAM_NAME = "pk"
ADDRESSES_URL = "addresses"
ADDRESS_NEW_URL = url_path(ADDRESSES_URL, "new")
ADDRESS_ID_URL = url_path(ADDRESSES_URL, f"<int:{PK_PARAM_NAME}>")
ADDRESSES_ID_DEFAULT_URL = \
    url_path(ADDRESSES_URL, f"<int:{PK_PARAM_NAME}>", "default")

# convention is addresses route names begin with 'address'
ADDRESSES_ROUTE_NAME = "addresses"
ADDRESS_NEW_ROUTE_NAME = "address_new"
ADDRESS_ID_ROUTE_NAME = "address_id"
ADDRESSES_ID_DEFAULT_ROUTE_NAME = "address_id_default"

# Address form related
LINE1_FIELD = 'line1'
LINE2_FIELD = 'line2'
CITY_FIELD = 'city'
LINE4_FIELD = 'state'
POSTCODE_FIELD = 'postcode'
SET_AS_DEFAULT_FIELD = "set_as_default"
