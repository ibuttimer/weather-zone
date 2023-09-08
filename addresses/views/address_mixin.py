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
from typing import Tuple, Dict, Any

from django.db import IntegrityError
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from addresses.constants import ADDRESS_SERVICE, MANAGE_DEFAULT_FUNC
from addresses.forms import AddressForm
from addresses.models import Address
from broker import ServiceCacheMixin, ServiceType
from forecast import GEOCODE_SERVICE, GEOCODE_ADDRESS_FUNC


DUPLICATE_ADDRESS_MSG = 'duplicate key value violates unique constraint'

ADDR_EXISTS = _('Address already exists')
CANT_SAVE_ADDR = _('Unable to save Address')


class AddressMixin(ServiceCacheMixin):
    """
    Mixin providing common address view-related functionality
    """
    INVALID = 0     # invalid form
    SUCCESS = 1     # saved
    NO_DEFAULT = 2  # no default address error
    DUPLICATE = 3   # duplicate address error

    def process_post(self, request: HttpRequest, address: Address = None,
                     *args, **kwargs
                     ) -> Tuple[int, Address, AddressForm, Dict[str, Any]]:
        """
        Process a http POST to create/update Address
        :param request: http request
        :param address: address to update
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """
        form = AddressForm(data=request.POST)

        status = self.INVALID
        addr_args = {}
        is_default = address.is_default if address else False

        if form.is_valid():

            set_as_default = form.get_field(AddressForm.SET_AS_DEFAULT_FIELD)
            if is_default and not set_as_default:
                # prevent default address change
                status = self.NO_DEFAULT
            else:
                # do geo query
                _, geocode_result = self.service(GEOCODE_SERVICE).execute(
                    GEOCODE_ADDRESS_FUNC, form.get_addr_fields_data())

                addr_args = Address.sanitise_param_dict(
                    geocode_result.as_dict())
                if address:
                    # update address
                    for key, val in addr_args.items():
                        setattr(address, key, val)
                else:
                    # create new address
                    address = Address(**addr_args)
                    address.user = request.user
                address.is_default = set_as_default

                # create/update object and manage default address
                try:
                    self.service(ADDRESS_SERVICE, stype=ServiceType.DB_CRUD) \
                        .execute(MANAGE_DEFAULT_FUNC, address, request=request,
                                 save_func=address.save)
                    # django autocommits changes
                    # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#autocommit
                    status = self.SUCCESS
                except IntegrityError as exc:
                    if DUPLICATE_ADDRESS_MSG in str(exc):
                        msg = ADDR_EXISTS   # duplicate address
                        status = self.DUPLICATE
                    else:
                        msg = CANT_SAVE_ADDR
                    form.add_error(None, msg)

        return status, address, form, addr_args
