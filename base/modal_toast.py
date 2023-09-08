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
from dataclasses import dataclass
from enum import Enum
from string import capwords
from typing import TypeVar, Union, Optional

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET

from weather_zone import ADMIN_URL, ROBOTS_URL
from utils import app_template_path

from .constants import (
    THIS_APP, REDIRECT_TO_CTX, SET_LANGUAGE_CTX, InfoModalLevel,
    MODAL_LEVEL_CTX, TITLE_CLASS_CTX, TOAST_POSITION_CTX
)

TITLE_CTX = 'title'
MESSAGE_CTX = 'message'
IDENTIFIER_CTX = 'identifier'
SHOW_INFO_CTX = 'show_info'
INFO_TOAST_CTX = 'info_toast'

REDIRECT_CTX = "redirect"                   # redirect url
REDIRECT_PAUSE_CTX = "pause"                # msec to wait before redirect
REWRITES_PROP_CTX = 'rewrites'              # multiple html rewrites
ELEMENT_SELECTOR_CTX = 'element_selector'   # element jquery selector
TOOLTIPS_SELECTOR_CTX = 'tooltips_selector'     # tooltips jquery selector
HTML_CTX = 'html'                           # html for rewrite
INNER_HTML_CTX = 'inner_html'               # inner html for rewrite
ENTITY_CTX = 'entity'                       # entity name

TypeInfoModalTemplate = \
    TypeVar("TypeInfoModalTemplate", bound="InfoModalTemplate")
TypeToastTemplate = \
    TypeVar("TypeToastTemplate", bound="ToastTemplate")


@dataclass(kw_only=True)
class InfoModalTemplate:
    """ Info modal template data """
    # require kw_only to avoid 'non-default argument follows default argument'
    # https://docs.python.org/3.10/library/dataclasses.html#module-contents
    template: str
    context: Optional[dict] = None
    request: Optional[HttpRequest] = None

    def make(self) -> str:
        """
        Render this template
        :return: rendered template or string
        """
        return self.render(self)

    @staticmethod
    def render(info: Union[str, TypeInfoModalTemplate]) -> str:
        """
        Render template
        :param info: modal template or string
        :return: rendered template or string
        """
        return render_to_string(
            info.template, context=info.context, request=info.request
        ) if isinstance(info, InfoModalTemplate) else info


def info_modal_payload(title: Union[str, InfoModalTemplate],
                       message: Union[str, InfoModalTemplate],
                       identifier: str, redirect_url: str = None) -> dict:
    """
    Generate payload for an info modal response.
    :param title: modal title
    :param message: modal message
    :param identifier: unique identifier
    :param redirect_url: url to redirect to when modal closes; default None
    :return: payload
    """
    if not identifier:
        identifier = ''
    return {
        SHOW_INFO_CTX: {
            TITLE_CTX: InfoModalTemplate.render(title),
            MESSAGE_CTX: InfoModalTemplate.render(message),
            REDIRECT_CTX: redirect_url or '',
            IDENTIFIER_CTX: identifier
        }
    }


def render_info_modal_title(level: InfoModalLevel) -> str:
    """
    Generate an info modal title html.
    :param level: modal title level
    :return: html
    """
    if isinstance(level, InfoModalLevel):
        if level == InfoModalLevel.NONE:
            title = ''
        else:
            modal_cfg = level.value[1]
            title = InfoModalTemplate(
                template=app_template_path(
                    THIS_APP, "snippet", "info_title.html"),
                context={
                    TITLE_CTX: capwords(modal_cfg.title_text),
                    MODAL_LEVEL_CTX: modal_cfg.name,
                    TITLE_CLASS_CTX: modal_cfg.title_class,
                }
            )
    else:
        raise ValueError(f"Invalid modal level: {level}")
    return InfoModalTemplate.render(title)


def level_info_modal_context(level: InfoModalLevel,
                             message: Union[str, InfoModalTemplate],
                             identifier: str,
                             redirect_url: str = None) -> dict:
    """
    Generate data for an info modal response.
    :param level: modal title level
    :param message: modal message
    :param identifier: unique identifier
    :param redirect_url: url to redirect to when modal closes; default None
    :return: response dict
    """
    return {
        TITLE_CTX: render_info_modal_title(level),
        MESSAGE_CTX: InfoModalTemplate.render(message),
        REDIRECT_CTX: redirect_url or '',
        IDENTIFIER_CTX: identifier
    }


def level_info_modal_payload(level: InfoModalLevel,
                             message: Union[str, InfoModalTemplate],
                             identifier: str,
                             redirect_url: str = None) -> dict:
    """
    Generate an info modal payload.
    :param level: modal title level
    :param message: modal message
    :param identifier: unique identifier
    :param redirect_url: url to redirect to when modal closes; default None
    :return: response dict
    """
    return {
        SHOW_INFO_CTX: level_info_modal_context(
            level, message, identifier, redirect_url=redirect_url)
    }


def render_level_info_modal(level: InfoModalLevel,
                            message: Union[str, InfoModalTemplate],
                            identifier: str,
                            redirect_url: str = None) -> dict:
    """
    Generate an info modal html.
    :param level: modal title level
    :param message: modal message
    :param identifier: unique identifier
    :param redirect_url: url to redirect to when modal closes; default None
    :return: response
    """
    return render_to_string(
        app_template_path(
            THIS_APP, "snippet", "info_modal.html"),
        context=level_info_modal_context(
            level, message, identifier, redirect_url=redirect_url)
    )


class ToastPosition(Enum):
    """
    Enum representing bootstrap toast positions
    https://getbootstrap.com/docs/5.3/components/toasts/#placement
    """
    TOP_LEFT = "top-0 start-0"
    TOP_CENTRE = "top-0 start-50 translate-middle-x"
    TOP_RIGHT = "top-0 end-0"
    MIDDLE_LEFT = "top-50 start-0 translate-middle-y"
    MIDDLE_CENTRE = "top-50 start-50 translate-middle"
    MIDDLE_RIGHT = "top-50 end-0 translate-middle-y"
    BOTTOM_LEFT = "bottom-0 start-0"
    BOTTOM_CENTRE = "bottom-0 start-50 translate-middle-x"
    BOTTOM_RIGHT = "bottom-0 end-0"


ToastPosition.DEFAULT = ToastPosition.TOP_RIGHT


@dataclass(kw_only=True)
class ToastTemplate(InfoModalTemplate):
    """ Toast template data """
    position: ToastPosition = ToastPosition.DEFAULT

    def make(self) -> str:
        """
        Render this template
        :return: rendered template or string
        """
        return self.render(self, position=self.position)

    @staticmethod
    def render(toast: Union[str, TypeToastTemplate],
               position: ToastPosition = ToastPosition.DEFAULT) -> str:
        """
        Render template
        :param toast: toast template or string
        :param position: display position; default ToastPosition.DEFAULT
        :return: rendered template or string
        """
        context = toast.context or {}
        context[TOAST_POSITION_CTX] = position.value
        return render_to_string(
            toast.template, context=context, request=toast.request
        ) if isinstance(toast, ToastTemplate) else toast


def info_toast_payload(
        message: Union[str, ToastTemplate],
        position: ToastPosition = ToastPosition.DEFAULT) -> dict:
    """
    Generate payload for an info toast response.
    :param message: toast message
    :param position: display position; default ToastPosition.DEFAULT
    :return: payload
    """
    return {
        INFO_TOAST_CTX: ToastTemplate.render(message),
        TOAST_POSITION_CTX: position.value
    }
