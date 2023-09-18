"""
User models
"""
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

from dataclasses import dataclass
import zlib
import json

from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

from utils import ModelMixin
from user.models import User

from .constants import (
    USER_FIELD, COUNTRY_FIELD, COMPONENTS_FIELD, FORMATTED_ADDR_FIELD,
    LATITUDE_FIELD, LONGITUDE_FIELD, IS_DEFAULT_FIELD, PLACE_ID_FIELD,
    GLOBAL_PLUS_CODE_FIELD
)


class CompressedTextField(models.BinaryField):
    """
    Compressed text field
    """

    def pre_save(self, model_instance, add):
        """
        Prepare the value before being saved to the database
        :param model_instance:
        :param add:
        :return:
        """
        byte_data = zlib.compress(super().pre_save(model_instance, add))
        # update the model’s attribute so that code holding references to the
        # model will always see the correct value
        # https://docs.djangoproject.com/en/4.2/howto/custom-model-fields/#preprocessing-values-before-saving
        setattr(model_instance, self.attname, byte_data)
        return byte_data

    def from_db_value(self, value, expression, connection):
        """
        Convert the value after being retrieved from the database
        :param value:
        :param expression:
        :param connection:
        :return:
        """
        if value is not None:
            value = zlib.decompress(value).decode()
        return value

    def to_python(self, value):
        return zlib.decompress(value).decode()


class CompressedJsonTextField(CompressedTextField):
    """
    Compressed text field
    """

    def pre_save(self, model_instance, add):
        """
        Prepare the value before being saved to the database
        :param model_instance:
        :param add:
        :return:
        """
        # get current value
        value = super(CompressedTextField, self).pre_save(model_instance, add)
        # update the model’s attribute so that the super class pre_save will
        # see the byte encoded value
        setattr(model_instance, self.attname, json.dumps(value).encode())
        return super().pre_save(model_instance, add)

    def from_db_value(self, value, expression, connection):
        """
        Convert the value after being retrieved from the database
        :param value:
        :param expression:
        :param connection:
        :return:
        """
        value = super().from_db_value(value, expression, connection)
        return json.loads(value) if value is not None else value

    def to_python(self, value):
        # If it's a string, it should be base64-encoded data
        return json.loads(super().to_python(value))


class Address(ModelMixin, models.Model):
    """
    Address model
    """
    # field names
    USER_FIELD = USER_FIELD
    COUNTRY_FIELD = COUNTRY_FIELD
    COMPONENTS_FIELD = COMPONENTS_FIELD
    FORMATTED_ADDR_FIELD = FORMATTED_ADDR_FIELD
    LATITUDE_FIELD = LATITUDE_FIELD
    LONGITUDE_FIELD = LONGITUDE_FIELD
    PLACE_ID_FIELD = PLACE_ID_FIELD
    GLOBAL_PLUS_CODE_FIELD = GLOBAL_PLUS_CODE_FIELD
    IS_DEFAULT_FIELD = IS_DEFAULT_FIELD

    COORDINATE_FIELDS = (LATITUDE_FIELD, LONGITUDE_FIELD,)

    ADDRESS_ATTRIB_COMPONENTS_MAX_LEN: int = 500
    ADDRESS_ATTRIB_FORMATTED_MAX_LEN: int = 250
    ADDRESS_ATTRIB_PLACE_ID_MAX_LEN: int = 250
    ADDRESS_ATTRIB_PLUS_CODE_MAX_LEN: int = 15

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    country = CountryField(blank_label=_('(Select country)'))

    # address components as a JSON string
    components = CompressedJsonTextField(
        _('Address components'),
        max_length=ADDRESS_ATTRIB_COMPONENTS_MAX_LEN, blank=False)
    formatted_addr = models.CharField(
        _('Formatted address'),
        max_length=ADDRESS_ATTRIB_FORMATTED_MAX_LEN, blank=False)
    latitude = models.FloatField(_('Latitude'), blank=False)
    longitude = models.FloatField(_('Longitude'), blank=False)
    place_id = CompressedTextField(
        _('Place ID'),
        max_length=ADDRESS_ATTRIB_PLACE_ID_MAX_LEN, blank=True)
    global_plus_code = models.CharField(
        _('Global Plus Code'),
        max_length=ADDRESS_ATTRIB_PLUS_CODE_MAX_LEN, blank=True)
    is_default = models.BooleanField(
        _('default'), default=False, blank=False, help_text=_(
            "Designates that this record represents the user's "
            "default address."
        ))

    @dataclass
    class Meta:
        """ Model metadata """
        unique_together = (LATITUDE_FIELD, LONGITUDE_FIELD,)
        ordering = [f'-{IS_DEFAULT_FIELD}']

    @classmethod
    def numeric_fields(cls) -> list[str]:
        """ Get the list of numeric fields """
        return [Address.LATITUDE_FIELD, Address.LONGITUDE_FIELD]

    @classmethod
    def boolean_fields(cls) -> list[str]:
        """ Get the list of boolean fields """
        return [Address.IS_DEFAULT_FIELD]

    def __str__(self):
        return f'{self.formatted_addr} {str(self.user)}'
