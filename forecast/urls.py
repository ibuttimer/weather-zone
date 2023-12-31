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
#

from django.urls import path

from .constants import (
    ADDRESS_URL, ADDRESS_ROUTE_NAME,
    LAT_LONG_URL, LAT_LONG_ROUTE_NAME,
    DISPLAY_URL, DISPLAY_ROUTE_NAME,
    DISPLAY_ADDRESS_URL, DISPLAY_ADDRESS_ROUTE_NAME,
    DASH_URL, DASH_ROUTE_NAME,
    THIS_APP,
)
from . import views


# https://docs.djangoproject.com/en/4.2/topics/http/urls/#url-namespaces-and-included-urlconfs
app_name = THIS_APP


urlpatterns = [
    # standard app urls
    path(ADDRESS_URL, views.ForecastAddress.as_view(), name=ADDRESS_ROUTE_NAME),
    # path(LAT_LONG_URL, views.UserDetailByUsername.as_view(),
    #      name=LAT_LONG_ROUTE_NAME),
    path(DISPLAY_ADDRESS_URL, views.ForecastAddressById.as_view(),
         name=DISPLAY_ADDRESS_ROUTE_NAME),
    path(DISPLAY_URL, views.display_forecast, name=DISPLAY_ROUTE_NAME),
    path(DASH_URL, views.display_home, name=DASH_ROUTE_NAME),
]
