"""
This file is used to create the views for the forecast app.
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
from typing import List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django_countries import countries

from base import TITLE_CTX, PAGE_HEADING_CTX, PAGE_SUB_HEADING_CTX
from forecast import (
    Registry, ALL_PROVIDERS, QUERY_PROVIDER, WeatherWarnings
)
from utils import (
    GET, app_template_path
)

from .constants import (
    THIS_APP, WARNING_LIST_CTX
)
from .dto import WeatherWarningsDo


@require_http_methods([GET])
def display_warnings(request: HttpRequest, country: str,
                     *args, **kwargs) -> HttpResponse:
    """
    Get weather warnings view function
    :param request: http request
    :param country: ISO 3166-1 alpha-2 country code
    :param args: additional arbitrary arguments
    :param kwargs: additional keyword arguments
    :return: http response
    """

    provider = request.GET.get(QUERY_PROVIDER, None)    # default is all
    if provider.lower() == ALL_PROVIDERS:
        provider = None    # default is all

    warnings = Registry.get_instance().generate_warnings(
        country, provider=provider)

    template_path, context = warnings_render_info(country, warnings)

    return render(request, template_path, context=context)


def warnings_render_info(country: str, warnings: List[WeatherWarnings]):
    """
    Get info to render a list of forecasts
    :param country: ISO 3166-1 alpha-2 country code
    :param warnings: WeatherWarnings list
    :return: tuple of template path and context
    """
    title = _("Weather warnings")
    heading = _("No weather warnings") if len(warnings) == 0 else title

    # for warn_list in warnings:
    #     warn_list.warnings = list(map(
    #         WarningItem.from_warning_entry, warn_list.warnings
    #     ))

    context = {
        TITLE_CTX: title,
        PAGE_HEADING_CTX: heading,
        PAGE_SUB_HEADING_CTX: dict(countries)[country],
        WARNING_LIST_CTX: [
            WeatherWarningsDo(ww) for ww in warnings
        ]
    }

    return app_template_path(THIS_APP, "warnings.html"), context
