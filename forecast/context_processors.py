"""
Context processors for the recipes app
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
from django.http import HttpRequest

from utils import resolve_req, add_navbar_attr, Crud
from .constants import (
    FORECAST_MENU_CTX, ADDRESS_ROUTE_NAME, LAT_LONG_ROUTE_NAME
)


def forecast_context(request: HttpRequest) -> dict:
    """
    Add user-specific context entries
    :param request: http request
    :return: dictionary to add to template context
    """
    context = {}
    called_by = resolve_req(request)
    if called_by:
        for ctx, check_func, is_dropdown_toggle in [
            (FORECAST_MENU_CTX, lambda name: name in [
                ADDRESS_ROUTE_NAME, LAT_LONG_ROUTE_NAME
            ], True),
        ]:
            add_navbar_attr(
                context, ctx, is_active=check_func(called_by.url_name),
                has_permission=True,
                is_dropdown_toggle=is_dropdown_toggle
            )

    return context
