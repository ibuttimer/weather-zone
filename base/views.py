"""
Views for base app
"""
#  MIT License
#
#  Copyright (c) 2022-2023 Ian Buttimer
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
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET

from weather_zone import ADMIN_URL, ROBOTS_URL, APP_NAME
from utils import app_template_path

from .constants import (
    THIS_APP, REDIRECT_TO_CTX, SET_LANGUAGE_CTX, TITLE_CTX, ABOUT_INFO_CTX,
    PROVIDERS_CTX, CREDITS_CTX, HELP_SECTIONS_CTX
)
from .credits import ICON_CREDITS, provider_credits

DISALLOWED_URLS = [
    ADMIN_URL,
]


@require_GET
def get_landing(request: HttpRequest) -> HttpResponse:
    """
    Render landing page
    :param request: request
    :return: response
    """
    return render(request, app_template_path(THIS_APP, 'landing.html'),
                  context={
                  })


@require_GET
def get_home(request: HttpRequest) -> HttpResponse:
    """
    Render home page
    :param request: request
    :return: response
    """
    return get_landing(request) \
        if not request.user or not request.user.is_authenticated else \
        redirect(settings.LOGIN_REDIRECT_URL)


@require_GET
def get_help(request: HttpRequest) -> HttpResponse:
    """
    Render help page
    :param request: request
    :return: response
    """
    from forecast import forecast_help
    from user import user_help

    help_sections = []
    help_sections.extend(forecast_help())
    help_sections.extend(user_help())
    context = {
        HELP_SECTIONS_CTX: help_sections,
    }
    return render(request, app_template_path(THIS_APP, 'help.html'),
                  context=context)


@require_GET
def get_about(request: HttpRequest) -> HttpResponse:
    """
    Render about page
    :param request: request
    :return: response
    """
    context = {
        TITLE_CTX: _('About %(app_name)s') % {'app_name': APP_NAME},
        ABOUT_INFO_CTX: _(
            '%(app_name)s is a weather forecast application utilising multiple '
            'third-party weather forecasters, to provide address-based weather '
            'forecasts.') % {'app_name': APP_NAME},
        PROVIDERS_CTX: provider_credits(),
        CREDITS_CTX: ICON_CREDITS,
    }
    return render(
        request, app_template_path(THIS_APP, "about.html"),
        context=context
    )


@require_GET
def get_privacy(request: HttpRequest) -> HttpResponse:
    """
    Render privacy page
    :param request: request
    :return: response
    """
    # return render(
    #     request, app_template_path(THIS_APP, "privacy.html")
    # )
    return get_landing(request)


@require_GET
def get_language(request: HttpRequest) -> HttpResponse:
    """
    Render set language page
    :param request: request
    :return: response
    """
    return render(
        request, app_template_path(THIS_APP, "set_language.html"), context={
            REDIRECT_TO_CTX: request.GET.get('next', '/'),
            SET_LANGUAGE_CTX: _('Set language'),
        }
    )


@require_GET
def robots_txt(request):
    """
    View function for robots.txt
    Based on https://adamj.eu/tech/2020/02/10/robots-txt/
    :param request: http request
    :return: robots.txt response
    """
    lines = [
        "User-Agent: *",
    ]
    lines.extend([
        f"Disallow: /{url}" for url in DISALLOWED_URLS
    ])
    lines.append(
        'Sitemap: {}'.format(
            request.build_absolute_uri().replace(ROBOTS_URL, 'sitemap.xml'))
    )
    return HttpResponse("\n".join(lines), content_type="text/plain")
