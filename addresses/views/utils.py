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
from typing import Union, List

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.conf import settings

from base import (
    render_level_info_modal, InfoModalLevel, InfoModalTemplate, IDENTIFIER_CTX
)
from ..constants import COUNT_CTX, THIS_APP
from ..models import Address
from utils import (
    Crud, permission_check, app_template_path
)


def address_permission_check(
        request: HttpRequest,
        perm_op: Union[Union[Crud, str], List[Union[Crud, str]]],
        raise_ex: bool = True) -> bool:
    """
    Check request user has specified permission
    :param request: http request
    :param perm_op: Crud operation or permission name to check
    :param raise_ex: raise exception; default True
    """
    return permission_check(request, Address, perm_op,
                            app_label=THIS_APP, raise_ex=raise_ex)


def address_dflt_unmod_snippets(count: int) -> List[str]:
    """
    Generate html snippets to display address default unmodifiable info modal
    :param count: number of addresses
    :return: list of html snippets
    """
    identifier = 'dflt-addr-unmod'
    return [
        render_level_info_modal(
            InfoModalLevel.WARN,
            InfoModalTemplate(
                template=app_template_path(
                    THIS_APP, "snippet",
                    "address_default_unmodifiable.html"),
                context={
                    COUNT_CTX: count,
                }
            ),
            identifier
        ),
        render_to_string(
            app_template_path(
                settings.BASE_APP_NAME, "snippet",
                "show_info_modal_on_ready.html"),
            context={
                IDENTIFIER_CTX: identifier
            }
        )
    ]
