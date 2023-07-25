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
from django.urls import path, include

from weather_zone import (
    HOME_ROUTE_NAME, HELP_URL, HELP_ROUTE_NAME,
    ABOUT_URL, ABOUT_ROUTE_NAME, PRIVACY_URL, PRIVACY_ROUTE_NAME,
    ROBOTS_URL, ROBOTS_ROUTE_NAME, LANGUAGE_URL, LANGUAGE_ROUTE_NAME,
)
from .views import (
    robots_txt, get_home,
    get_about, get_privacy, get_help, get_language
)

_url_info = [
    # url, endpoint, route name
    (ABOUT_URL, get_about, ABOUT_ROUTE_NAME),
    (HELP_URL, get_help, HELP_ROUTE_NAME),
    (PRIVACY_URL, get_privacy, PRIVACY_ROUTE_NAME),
    (LANGUAGE_URL, get_language, LANGUAGE_ROUTE_NAME),
    ('', get_home, HOME_ROUTE_NAME),
]

urlpatterns = [
    path(ROBOTS_URL, robots_txt, name=ROBOTS_ROUTE_NAME),
    path("i18n/", include("django.conf.urls.i18n")),
]
urlpatterns.extend([
    # standard urls
    path(url, endpoint, name=route) for url, endpoint, route in _url_info
])
