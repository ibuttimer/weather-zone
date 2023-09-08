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
from typing import Any, Callable, Union, Dict

from django.db.models import Model
from django.http import HttpRequest

from broker import ICrudService
from forecast import GeoCodeResult
from utils import SingletonMixin, ModelMixin
from user.models import User

from .models import Address
from .views import addresses_query


class AddressService(SingletonMixin, ICrudService):
    """
    Address service
    """

    model: Union[ModelMixin, Model] = Address

    USER_LAT_LNG_FIELDS = {Address.USER_FIELD, Address.LATITUDE_FIELD,
                           Address.LONGITUDE_FIELD}
    USER_DFLT_FIELDS = {Address.USER_FIELD, Address.IS_DEFAULT_FIELD}
    ID_FIELDS = {Address.id_field()}

    def create(self, user: User, geocode_result: GeoCodeResult, *args,
               **kwargs) -> Any:
        """
        Create an address.
        User, latitude and longitude are required arguments.

        :param user: user to associate with address
        :param geocode_result: geocode result to create address from
        :param args: arguments
        :param kwargs: keyword arguments to filter by
        :return: Optional[Address]
        """
        addr_args = geocode_result.as_dict()

        addr_args[Address.USER_FIELD] = user
        addr = Address(**Address.sanitise_param_dict(addr_args))

        manage_default(addr, save_func=addr.save)
        return addr

    def get(self, *args, free_seek: bool = False, **kwargs) -> Any:
        """
        Get an address; returning None if not found.

        :param args: arguments
        :param free_seek: allow free seek; default False
        :param kwargs: keyword arguments to filter by
            non free seek mode:
                user: user to associate with address
                latitude: location latitude
                longitude: location longitude
                or
                user: user to associate with address
                is_default: is default address
                or
                id: address id
        :return: Optional[Address]
        :raises: Model.MultipleObjectsReturned if multiple objects found
        :raises: ValueError any required arguments are not specified
        """
        query_args = kwargs.copy()

        if not free_seek:
            key_set = set(kwargs.keys())

            if not any([
                self.USER_LAT_LNG_FIELDS.issubset(key_set),
                self.USER_DFLT_FIELDS.issubset(key_set),
                self.ID_FIELDS.issubset(key_set),
            ]):
                raise ValueError(f'Unknown query: {key_set}')

        return self.model.get_by_fields(
            get_or_404=False, does_not_exit_none=True, **query_args)

    def update(self, *args, update: Dict, **kwargs) -> Any:
        """
        Update address(es).
        :param args: arguments
        :param update: update values
        :param kwargs: keyword arguments to filter by
        :return: number of affected rows
        """
        query = Address.objects.filter(**kwargs)
        affected = 0
        will_affect = query.count()
        clear_default = update.get(Address.IS_DEFAULT_FIELD, None) is False

        if will_affect == 1:
            # only one address to update
            address = query.first()
            if address.is_default and clear_default:
                # need a default address
                raise ValueError(
                    'Default address required, set another address as default '
                    'first')

            affected = query.update(**update)
            manage_default(address, save_func=address.save)

        if will_affect > 1:
            if update.get(Address.IS_DEFAULT_FIELD, False):
                # can't have multiple default addresses
                raise ValueError('Multiple default addresses not allowed')

            # TODO - check updating multiple addresses will result in no default

            affected = query.update(**update)

        return affected

    def delete(self, *args, **kwargs) -> Any:
        pass


def manage_default(instance: Address, request: HttpRequest = None,
                   save_func: Callable = None):
    """
    Manage default address for user.
    Note: If `request` is None, the address instance user is used.
    :param instance: address being added/updated
    :param request: http request; default None
    :param save_func: save instance function; default None
    """
    addr_ids = None     # ids of existing addresses

    addr_query = addresses_query(
        user=request.user if request else instance.user)
    if not addr_query.exists():
        # only address so set as default
        instance.is_default = True
    else:
        if instance.is_default:
            # setting new address as default, so clear default
            # on existing
            if instance.pk:
                addr_query = addr_query.exclude(**{
                    f'{Address.id_field()}': instance.pk
                })

            addr_ids = list(
                addr_query.values_list(Address.id_field(), flat=True)
            )

    if save_func:
        save_func()

    if addr_ids:
        # clear default on existing addresses
        Address.objects.filter(**{
            f'{Address.id_field()}__in': addr_ids
        }).update(**{
            f'{Address.IS_DEFAULT_FIELD}': False
        })


# add AddressService-specific methods to AddressService class
AddressService.manage_default = ICrudService.make_api_method(manage_default)
