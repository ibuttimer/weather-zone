""" Permissions related utility functions """
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
from typing import Union, List

from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpRequest
from django.template.defaultfilters import pluralize

from .misc import Crud, ensure_list
from .models import ModelMixin
from .url_path import GET, PATCH, POST, DELETE


def permission_name(
        model: [str, models.Model], perm_op: Union[Crud, str],
        app_label: str = None
) -> str:
    """
    Generate a permission name.
    See
    https://docs.djangoproject.com/en/4.1/topics/auth/default/#default-permissions
    :param model: model or model name
    :param perm_op: Crud operation or permission name to check
    :param app_label:
        app label for models defined outside of an application in
        INSTALLED_APPS, default none
    :return: permission string;
            `{<app_label>.}[add|change|delete|view]_<model>`
    """
    perm = f'{app_label}.' if app_label else ''
    if not isinstance(model, str):
        model = model._meta.model_name  # pylint: disable=protected-access
    if isinstance(perm_op, Crud):
        perm_val = perm_op.value[0] if isinstance(perm_op.value, tuple) \
            else perm_op.value
    else:
        perm_val = perm_op
    return f'{perm}{perm_val}_{model}'


def permission_check(
        request: Union[HttpRequest], model: [str, models.Model],
        perm_op: Union[Union[Crud, str], List[Union[Crud, str]]],
        app_label: str = None, raise_ex: bool = False) -> bool:
    """
    Check request user has specified permission
    :param request: http request or user
    :param model: model or model name
    :param perm_op: Crud operation or permission name to check
    :param app_label:
        app label for models defined outside an application in
        INSTALLED_APPS, default none
    :param raise_ex: raise exception; default False
    :return: True if user has permission
    :raises PermissionDenied if user does not have permission and `raise_ex`
        is True
    """
    user = request.user if isinstance(request, HttpRequest) else request
    has_perm = user.is_superuser
    if not has_perm:
        for chk_perm in ensure_list(perm_op):
            has_perm = user.has_perm(
                permission_name(model, chk_perm, app_label=app_label))
            if not has_perm:
                break

        if not has_perm and raise_ex:
            raise PermissionDenied("Insufficient permissions")
    return has_perm


ACTIONS = {
    GET: 'viewed',
    PATCH: 'updated',
    POST: 'updated',
    DELETE: 'deleted'
}


def raise_permission_denied(
        request: HttpRequest, model: Union[ModelMixin, str],
        plural: str = 's'):
    """
    Raise a PermissionDenied exception
    :param request: http request
    :param model: model
    :param plural: model name pluralising addition; default 's'
        (https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#pluralize)
    :raises: PermissionDenied
    """
    if isinstance(model, ModelMixin):
        model = model.model_name_caps()
    action = ACTIONS[request.method.upper()]
    raise PermissionDenied(
        f"{model}{pluralize(2, arg=plural)} may only be {action} by "
        f"their owners")
