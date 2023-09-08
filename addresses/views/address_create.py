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
from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

from base.constants import SUBMIT_BTN_TEXT
from utils import (
    Crud, READ_ONLY_CTX, SUBMIT_URL_CTX, app_template_path, reverse_q,
    namespaced_url, TITLE_CTX, redirect_on_success_or_render,
    PAGE_HEADING_CTX, SUBMIT_BTN_TEXT_CTX, USER_QUERY
)
from .address_mixin import AddressMixin

from ..constants import (
    THIS_APP, ADDRESS_FORM_CTX, ADDRESS_NEW_ROUTE_NAME, ADDRESSES_ROUTE_NAME
)
from ..forms import AddressForm
from ..models import Address

from .utils import address_permission_check


TITLE_NEW = _('New Address')


class AddressCreate(AddressMixin, LoginRequiredMixin, View):
    """
    Class-based view for address creation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        GET method for Address
        :param request: http request
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """
        address_permission_check(request, Crud.CREATE)

        template_path, context = self.render_info(AddressForm())

        return render(request, template_path, context=context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        POST method to update Opinion
        :param request: http request
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """
        address_permission_check(request, Crud.CREATE)

        status, _, form, _ = self.process_post(
            request, *args, **kwargs)

        if status == self.SUCCESS:
            # success
            redirect_to = get_user_addresses_url(request)
            template_path, context = None, None
        else:
            # invalid form or duplicate
            redirect_to = None
            template_path, context = self.render_info(form)

        return redirect_on_success_or_render(
            request, redirect_to is not None, redirect_to=redirect_to,
            template_path=template_path, context=context)

    def render_info(self, form: AddressForm):
        """
        Get info to render an address form
        :param form: form to use
        :return: tuple of template path and context
        """
        return for_address_form_render(
            TITLE_NEW, Crud.CREATE, **{
                SUBMIT_URL_CTX: self.url(),
                ADDRESS_FORM_CTX: form
            })

    def url(self) -> str:
        """
        Get url for address creation
        :return: url
        """
        return reverse_q(
            namespaced_url(THIS_APP, ADDRESS_NEW_ROUTE_NAME)
        )


def for_address_form_render(
        title: str, action: Crud, **kwargs: object
) -> tuple[str, dict[str, Address | list[str] | AddressForm | bool]]:
    """
    Get the template and context to Render the address template
    :param title: title
    :param action: form action
    :param kwargs: context keyword values, see get_opinion_context()
    :return: tuple of template path and context
    """
    context = {
        TITLE_CTX: title,
        PAGE_HEADING_CTX: title,
        SUBMIT_BTN_TEXT_CTX: SUBMIT_BTN_TEXT[action],
        READ_ONLY_CTX: kwargs.get(READ_ONLY_CTX, False),
    }

    context_form = kwargs.get(ADDRESS_FORM_CTX, None)
    if context_form:
        context[ADDRESS_FORM_CTX] = context_form
        context[SUBMIT_URL_CTX] = kwargs.get(SUBMIT_URL_CTX, None)

    return app_template_path(THIS_APP, "address_form.html"), context


def get_user_addresses_url(
        request: HttpRequest, query_kwargs: Optional[dict] = None):
    """
    Get the addresses url for a user
    :param request: http request
    :param query_kwargs: additional query args; default None
    :return: url
    """
    if not query_kwargs:
        query_kwargs = {}
    query_kwargs[USER_QUERY] = request.user.username
    return reverse_q(
        namespaced_url(THIS_APP, ADDRESSES_ROUTE_NAME),
        query_kwargs=query_kwargs
    )
