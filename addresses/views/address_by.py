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
from http import HTTPStatus
from typing import Tuple, Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_http_methods

from base import (
    InfoModalLevel, InfoModalTemplate, level_info_modal_payload,
    redirect_payload, entity_delete_result_payload,
)
from broker import Broker, ServiceType
from forecast import GeoCodeResult
from utils import (
    Crud, SUBMIT_URL_CTX, app_template_path, reverse_q,
    namespaced_url, redirect_on_success_or_render, PATCH,
    raise_permission_denied
)
from .address_mixin import AddressMixin
from ..constants import (
    ADDRESS_FORM_CTX, ADDRESS_ID_ROUTE_NAME, COUNT_CTX, THIS_APP,
    ADDRESS_SERVICE, MANAGE_DEFAULT_FUNC, ADDRESSES_ROUTE_NAME
)
from ..forms import AddressForm
from ..models import Address
from .address_create import (
    for_address_form_render, get_user_addresses_url
)
from .address_queries import addresses_query, DEFAULT_ADDRESS_QUERY
from .utils import address_permission_check

TITLE_UPDATE = _('Update Address')


class AddressDetail(AddressMixin, LoginRequiredMixin, View):
    """
    Class-based view for address get/update/delete
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request: HttpRequest, pk: int,
            *args, **kwargs) -> HttpResponse:
        """
        GET method for Address
        :param request: http request
        :param pk: id of address
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """
        address_permission_check(request, Crud.UPDATE)

        address, _ = get_address(pk)

        own_address_check(request, address)
        form = AddressForm(initial=address_form_initial(address))
        form.fields[AddressForm.SET_AS_DEFAULT_FIELD].disabled = \
            addresses_query(request.user).count() == 1

        template_path, context = self.render_info(form, pk=pk)

        return render(request, template_path, context=context)

    def post(self, request: HttpRequest, pk: int,
             *args, **kwargs) -> HttpResponse:
        """
        POST method to update Address
        :param request: http request
        :param pk: id of address
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """
        address_permission_check(request, Crud.UPDATE)

        address, _ = get_address(pk)
        is_default = address.is_default

        own_address_check(request, address)

        query_kwargs = {}
        status, address, form, _ = self.process_post(
            request, address=address, *args, **kwargs)

        if status != self.INVALID:
            # success or no default address
            if status == self.NO_DEFAULT:
                # prevent default address change; display info modal
                form.set_as_default = is_default
                query_kwargs = {
                    DEFAULT_ADDRESS_QUERY:
                        addresses_query(request.user).count(),
                }
                # TODO alternative to passing default addr query param
                # passing default addr query param means that a reload
                # displays the modal again but can't pass a context to
                # redirect so ?

            redirect_to = get_user_addresses_url(
                request, query_kwargs=query_kwargs)
            template_path, context = None, None
        else:
            redirect_to = None
            template_path, context = self.render_info(form)

        return redirect_on_success_or_render(
            request, redirect_to is not None, redirect_to=redirect_to,
            template_path=template_path, context=context)

    def render_info(self, form: AddressForm, pk: int = None) -> tuple[
            str, dict[str, Address | list[str] | AddressForm | bool]]:
        """
        Get info to render an address entry
        :param form: form to use
        :param pk: id of address; default None
        :return: tuple of template path and context
        """
        return for_address_form_render(
            TITLE_UPDATE, Crud.UPDATE, **{
                SUBMIT_URL_CTX: self.url(pk or 0),
                ADDRESS_FORM_CTX: form
            })

    def delete(self, request: HttpRequest, pk: int,
               *args, **kwargs) -> HttpResponse:
        """
        DELETE method to delete Address
        :param request: http request
        :param pk: id of address
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """
        address_permission_check(request, Crud.UPDATE)

        address, _ = get_address(pk)

        own_address_check(request, address)

        status = HTTPStatus.OK
        if address.is_default:
            # prevent default address delete; display info modal
            payload = level_info_modal_payload(
                InfoModalLevel.WARN,
                InfoModalTemplate(
                    template=app_template_path(
                        THIS_APP, "snippet",
                        "default_address_undeletable.html"),
                    context={
                        COUNT_CTX: addresses_query(request.user).count(),
                    }
                ),
                'dflt-addr-del'
            )
        else:
            # delete address
            count, _ = address.delete()
            payload = entity_delete_result_payload(
                "#id__address-deleted-modal-body", count > 0, 'address')

            if count == 0:
                status = HTTPStatus.BAD_REQUEST

        return JsonResponse(payload, status=status)

    def url(self, pk: int) -> str:
        """
        Get url for address update/delete
        :param pk: id of entity
        :return: url
        """
        return reverse_q(
            namespaced_url(THIS_APP, ADDRESS_ID_ROUTE_NAME), args=[pk]
        ) if pk else reverse_q(
            namespaced_url(THIS_APP, ADDRESSES_ROUTE_NAME)
        )


def get_address(pk: int) -> Tuple[Address, dict]:
    """
    Get address by specified `id`
    :param pk: id of address
    :return: tuple of object and query param
    """
    query_param = {
        f'{Address.id_field()}': pk
    }
    entity = get_object_or_404(Address, **query_param)
    return entity, query_param


@login_required
@require_http_methods([PATCH])
def address_default(request: HttpRequest, pk: int) -> HttpResponse:
    """
    View function to update opinion status.
    :param request: http request
    :param pk:      id of opinion
    :return: response
    """
    address_permission_check(request, Crud.UPDATE)

    address, _ = get_address(pk)

    own_address_check(request, address)

    address.is_default = True

    # update object
    Broker.get_instance() \
        .get(ADDRESS_SERVICE, service_type=ServiceType.DB_CRUD) \
        .execute(MANAGE_DEFAULT_FUNC, address, request=request,
                 save_func=address.save)

    return JsonResponse(
        redirect_payload(
            get_user_addresses_url(request)
        ),
        status=HTTPStatus.OK
    )


def own_address_check(request: HttpRequest, address: Address,
                      raise_ex: bool = True) -> bool:
    """
    Check request user is address owner
    :param request: http request
    :param address: address
    :param raise_ex: raise exception if not own; default True
    """
    is_own = request.user.id == address.user.id
    if not is_own and raise_ex:
        raise_permission_denied(request, address, plural='es')

    return is_own


def address_form_initial(address: Address) -> Dict:
    """
    Get initial values for address form
    :param address: address
    :return: dict of initial values
    """
    return {
        AddressForm.LINE1_FIELD: GeoCodeResult.line1_from_components(
            address.components),
        AddressForm.LINE2_FIELD: GeoCodeResult.line2_from_components(
            address.components),
        AddressForm.CITY_FIELD: GeoCodeResult.locality_from_components(
            address.components),
        AddressForm.STATE_FIELD: GeoCodeResult.state_from_components(
            address.components),
        AddressForm.POSTCODE_FIELD: GeoCodeResult.postcode_from_components(
            address.components),
        AddressForm.COUNTRY_FIELD: address.country,
        AddressForm.SET_AS_DEFAULT_FIELD: address.is_default,
    }
