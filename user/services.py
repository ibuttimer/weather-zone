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
from typing import Optional, Any, Callable, Union, Dict
import json

from django.db.models import Model

from broker import ICrudService
from forecast import GeoCodeResult
from utils import SingletonMixin, ModelMixin

from .models import User, Address


class AddressService(SingletonMixin, ICrudService):
    """
    Address service
    """

    model: Union[ModelMixin, Model] = Address

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
        addr = Address(**addr_args)

        manage_default(
            addr, save_func=lambda: addr.save())
        return addr

    def get(self, *args, **kwargs) -> Any:
        """
        Get an address; returning None if not found.

        :param args: arguments
        :param kwargs: keyword arguments to filter by
            user: user to associate with address
            latitude: location latitude
            longitude: location longitude
            or
            id: address id
        :return: Optional[Address]
        :raises: Model.MultipleObjectsReturned if multiple objects found
        :raises: ValueError any requires arguments are not specified
        """
        query_args = kwargs.copy()
        errors = []
        for field in [
            Address.USER_FIELD, Address.LATITUDE_FIELD, Address.LONGITUDE_FIELD
        ]:
            if field not in kwargs:
                errors.append(field)
        if len(errors) > 0 and Address.id_field() not in kwargs:
            raise ValueError(f'{", ".join(errors)} must be specified')

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
        return Address.objects.filter(**kwargs).update(**update) \
            if len(update) > 0 else 0

    def delete(self, *args, **kwargs) -> Any:
        pass

    def execute(self, func: str, *args, **kwargs) -> Any:
        pass


def manage_default(instance: Address, save_func: Callable = None):
    """
    Manage default address for user
    :param instance: address being added/updated
    :param save_func: save instance function; default None
    """
    addr_ids = None     # ids of existing addresses

    addr_query = Address.objects.filter(**{
        f'{Address.USER_FIELD}': instance.user
    })
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
