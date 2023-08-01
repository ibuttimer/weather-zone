"""
Constants for locationforecast app
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


# name of this app
THIS_APP = Path(__file__).resolve().parent.name

# prefix for environment variables
APP_ENV_PREFIX = f'{THIS_APP.upper()}_'

# legend data keys and attributes
OLD_ID_PROP = 'old_id'
VARIANTS_PROP = 'variants'

# forcast data tags (standardised to lower case)
# and attributes (following conversion to dict by xmltodict)
CREATED_PATH = ['weatherdata', '@created']
FORECAST_DATA_PATH = ['weatherdata', 'product', 'time']
DATATYPE_ATTRIB = '@datatype'
FROM_ATTRIB = '@from'
TO_ATTRIB = '@to'

FORECAST_PROP = 'forecast'
LOCATION_PROP = 'location'
TEMPERATURE_TAG = 'temperature'
WIND_DIRECTION_TAG = 'winddirection'
WIND_SPEED_TAG = 'windspeed'
WIND_GUST_TAG = 'windgust'
HUMIDITY_TAG = 'humidity'
PRESSURE = 'pressure'
CLOUDINESS = 'cloudiness'
FOG = 'fog'
LOWCLOUDS = 'lowclouds'
MEDIUMCLOUDS = 'mediumclouds'
HIGHCLOUDS = 'highclouds'
DEWPOINTTEMPERATURE = 'dewpointtemperature'
PRECIPITATION_TAG = 'precipitation'
SYMBOL_TAG = 'symbol'

ALTITUDE_PROP = '@altitude'
LATITUDE_PROP = '@latitude'
LONGITUDE_PROP = '@longitude'
UNIT_ATTRIB = '@unit'
VALUE_ATTRIB = '@value'
NAME_ATTRIB = '@name'
DEG_ATTRIB = '@deg'
MPS_ATTRIB = '@mps'
PERCENT_ATTRIB = '@percent'
ATTRIB_MARKER = '@'     # char xmltodict prepends to xml tag attributes
LITERAL_MARKER = '$'
PERCENT_LITERAL = f'{LITERAL_MARKER}percent'
PROBABILITY_ATTRIB = '@probability'
NUM_ATTRIB = '@number'
ID_ATTRIB = '@id'
