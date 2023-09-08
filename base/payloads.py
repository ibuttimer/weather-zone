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
from typing import Optional

from django.template.loader import render_to_string

from utils import app_template_path, STATUS_CTX

from .constants import THIS_APP

REDIRECT_CTX = "redirect"                   # redirect url
REDIRECT_PAUSE_CTX = "pause"                # msec to wait before redirect
REWRITES_PROP_CTX = 'rewrites'              # multiple html rewrites
ELEMENT_SELECTOR_CTX = 'element_selector'   # element jquery selector
TOOLTIPS_SELECTOR_CTX = 'tooltips_selector'     # tooltips jquery selector
HTML_CTX = 'html'                           # html for rewrite
INNER_HTML_CTX = 'inner_html'               # inner html for rewrite
ENTITY_CTX = 'entity'                       # entity name


def redirect_payload(url: str, pause: int = 0,
                     extra: Optional[dict] = None) -> dict:
    """
    Generate payload for a redirect response.
    :param url: url to redirect to
    :param pause: msec pause before redirect; default None
    :param extra: extra payload content; default None
    :return: response
    """
    payload = {
        REDIRECT_CTX: url
    }
    if pause > 0:
        payload[REDIRECT_PAUSE_CTX] = pause
    if isinstance(extra, dict):
        payload.update(extra)

    return payload


def _html_payload(selector: str, html: str, key: str,
                  tooltips_selector: Optional[str] = None,
                  extra: Optional[dict] = None) -> dict:
    """
    Generate payload for a replace html response.
    :param selector: element jquery selector
    :param html: replacement html
    :param tooltips_selector: tooltips jquery selector; default None
    :param extra: extra payload content; default None
    :return: response
    """
    payload = {
        ELEMENT_SELECTOR_CTX: selector,
        key: html
    }
    if tooltips_selector:
        payload[TOOLTIPS_SELECTOR_CTX] = tooltips_selector
    if isinstance(extra, dict):
        payload.update(extra)

    return payload


def replace_html_payload(selector: str, html: str,
                         tooltips_selector: Optional[str] = None,
                         extra: Optional[dict] = None) -> dict:
    """
    Generate payload for a replace html response.
    :param selector: element jquery selector
    :param html: replacement html
    :param tooltips_selector: tooltips jquery selector; default None
    :param extra: extra payload content; default None
    :return: response
    """
    return _html_payload(selector, html, HTML_CTX,
                         tooltips_selector=tooltips_selector, extra=extra)


def replace_inner_html_payload(selector: str, html: str,
                               tooltips_selector: Optional[str] = None,
                               extra: Optional[dict] = None) -> dict:
    """
    Generate payload for a replace inner html response.
    :param selector: element jquery selector
    :param html: replacement html
    :param tooltips_selector: tooltips jquery selector; default None
    :param extra: extra payload content; default None
    :return: response
    """
    return _html_payload(selector, html, INNER_HTML_CTX,
                         tooltips_selector=tooltips_selector, extra=extra)


def rewrite_payload(*args, extra: Optional[dict] = None) -> dict:
    """
    Generate payload for a rewrite html response.
    :param args: replace html payloads
    :param extra: extra payload content; default None
    :return: response
    """
    payload = {
        REWRITES_PROP_CTX: [arg for arg in args if arg]
    }
    if isinstance(extra, dict):
        payload.update(extra)

    return payload


def entity_delete_result_payload(
        selector: str, status: bool, entity: str,
        extra: Optional[dict] = None) -> dict:
    """
    Generate payload for an entity delete html response.
    :param selector: element jquery selector
    :param status: delete result
    :param entity: entity name
    :param extra: extra payload content; default None
    :return: response
    """
    return replace_inner_html_payload(
        selector, render_to_string(
            app_template_path(
                THIS_APP, "snippet", "entity_delete_result.html"),
            context={
                STATUS_CTX: status,
                ENTITY_CTX: entity
            }
        ), extra=extra
    )
