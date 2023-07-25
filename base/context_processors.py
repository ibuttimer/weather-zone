"""
Base context processors
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
#
from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import (
    get_language_from_request, gettext_lazy as _
)

from django_countries.fields import Country

from weather_zone.constants import (
    HOME_MENU_CTX, HOME_ROUTE_NAME,
    HELP_MENU_CTX, HELP_ROUTE_NAME,
    ABOUT_MENU_CTX, ABOUT_ROUTE_NAME,
    APP_NAME, NO_ROBOTS_CTX
)
from utils import resolve_req, add_navbar_attr

from .constants import APP_NAME_CTX, LANG_COUNTRY_CTX, ARIA_CHANGE_LANG_CTX

LANG_COUNTRIES = {
    'en': Country(code='GB'),
    'de': Country(code='DE'),
    'fr': Country(code='FR'),
}
assert set(LANG_COUNTRIES.keys()) == set(
    map(lambda x: x[0], settings.LANGUAGES))


def base_context(request: HttpRequest) -> dict:
    """
    Add base-specific context entries
    :param request: http request
    :return: dictionary to add to template context
    """
    context = {
        APP_NAME_CTX: APP_NAME,
        LANG_COUNTRY_CTX: LANG_COUNTRIES[
            get_language_from_request(request, check_path=False).lower()
        ],
        ARIA_CHANGE_LANG_CTX: _('Change language'),
    }
    no_robots = False
    called_by = resolve_req(request)
    if called_by:
        for ctx, routes in [
            (HOME_MENU_CTX, [
                HOME_ROUTE_NAME
            ]),
            (HELP_MENU_CTX, [HELP_ROUTE_NAME]),
            (ABOUT_MENU_CTX, [ABOUT_ROUTE_NAME]),
        ]:
            add_navbar_attr(
                context, ctx, is_active=called_by.url_name in routes)

        # set no robots
        # allauth route names start with 'account_' and have no app name
        no_robots = called_by.app_name == '' and \
            called_by.url_name.startswith('account_')
        # admin routes have app name 'admin'
        no_robots = no_robots or called_by.app_name == 'admin'

    context.update({
        NO_ROBOTS_CTX: no_robots
    })

    return context
