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
from .constants import (
    HOME_URL, HOME_ROUTE_NAME, ADMIN_URL,
    HELP_URL, HELP_ROUTE_NAME, ABOUT_URL, ABOUT_ROUTE_NAME,
    PRIVACY_URL, PRIVACY_ROUTE_NAME, ROBOTS_URL, ROBOTS_ROUTE_NAME,
    LANGUAGE_URL, LANGUAGE_ROUTE_NAME,
    SITEMAP_URL, APP_NAME,
    BASE_APP_NAME, FORECAST_APP_NAME, LOCATIONFORECAST_APP_NAME,
    WARNING_APP_NAME, USER_APP_NAME, ADDRESSES_APP_NAME
)
from .misc import provider_settings_name


__all__ = [
    'HOME_URL',
    'HOME_ROUTE_NAME',
    'ADMIN_URL',
    'HELP_URL',
    'HELP_ROUTE_NAME',
    'ABOUT_URL',
    'ABOUT_ROUTE_NAME',
    'PRIVACY_URL',
    'PRIVACY_ROUTE_NAME',
    'ROBOTS_URL',
    'ROBOTS_ROUTE_NAME',
    'LANGUAGE_URL',
    'LANGUAGE_ROUTE_NAME',
    'SITEMAP_URL',
    'APP_NAME',

    'BASE_APP_NAME',
    'FORECAST_APP_NAME',
    'LOCATIONFORECAST_APP_NAME',
    'WARNING_APP_NAME',
    'USER_APP_NAME',
    'ADDRESSES_APP_NAME',

    'provider_settings_name',
]
