"""
User models
"""
from dataclasses import dataclass

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

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from utils import ModelMixin

from .constants import (
    FIRST_NAME, LAST_NAME, PREVIOUS_LOGIN
)


class User(ModelMixin, AbstractUser):
    """
    Custom user model
    (Recommended by
    https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#auth-custom-user)
    """

    # field names
    FIRST_NAME_FIELD = FIRST_NAME
    LAST_NAME_FIELD = LAST_NAME
    # EMAIL_FIELD and USERNAME_FIELD inherited from AbstractUser
    PASSWORD_FIELD = 'password'
    PREVIOUS_LOGIN_FIELD = PREVIOUS_LOGIN

    # Values copied from django.contrib.auth.models.py::AbstractUser
    USER_ATTRIB_FIRST_NAME_MAX_LEN: int = 150
    USER_ATTRIB_LAST_NAME_MAX_LEN: int = 150
    USER_ATTRIB_USERNAME_MAX_LEN: int = 150
    # Values copied from django.db.models.fields::EmailField
    USER_ATTRIB_EMAIL_MAX_LEN: int = 254

    # by the time the 'user_logged_in' signal is received the 'last_login'
    # field in AbstractBaseUser has already been updated to the current login
    previous_login = models.DateTimeField(
        _("previous login"), blank=True, null=True)

    @dataclass
    class Meta:
        """ Model metadata """
        ordering = ["date_joined"]

    def __str__(self):
        return self.username


# class Address(ModelMixin, models.Model):
#     """
#     Address model
#     """
#     # field names
#     USER_FIELD = USER_FIELD
#     COUNTRY_FIELD = COUNTRY_FIELD
#     STREET_FIELD = STREET_FIELD
#     STREET2_FIELD = STREET2_FIELD
#     CITY_FIELD = CITY_FIELD
#     STATE_FIELD = STATE_FIELD
#     POSTCODE_FIELD = POSTCODE_FIELD
#     IS_DEFAULT_FIELD = IS_DEFAULT_FIELD
#
#     ADDRESS_ATTRIB_STREET_MAX_LEN: int = 150
#     ADDRESS_ATTRIB_STREET2_MAX_LEN: int = 150
#     ADDRESS_ATTRIB_CITY_MAX_LEN: int = 50
#     ADDRESS_ATTRIB_STATE_MAX_LEN: int = 50
#     ADDRESS_ATTRIB_POSTCODE_MAX_LEN: int = 50
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     components = models.CharField(
#         _('address components'), max_length=ADDRESS_ATTRIB_STREET_MAX_LEN,
#         blank=False)
#     street2 = models.CharField(
#         _('street address line 2'), max_length=ADDRESS_ATTRIB_STREET2_MAX_LEN,
#         blank=True)
#     city = models.CharField(
#         _('city'), max_length=ADDRESS_ATTRIB_CITY_MAX_LEN,
#         blank=True)
#     state = models.CharField(
#         _('state'), max_length=ADDRESS_ATTRIB_STATE_MAX_LEN,
#         blank=True)
#     postcode = models.CharField(
#         _('postcode'), max_length=ADDRESS_ATTRIB_POSTCODE_MAX_LEN,
#         blank=True)
#     is_default = models.BooleanField(
#         _('default'), default=False, blank=False, help_text=_(
#             "Designates that this record represents the user's "
#             "default address."
#         ))
#
#     @dataclass
#     class Meta:
#         """ Model metadata """
#         ordering = [f'-{IS_DEFAULT_FIELD}']
#
#     @classmethod
#     def boolean_fields(cls) -> list[str]:
#         """ Get the list of boolean fields """
#         return [Address.IS_DEFAULT_FIELD]
#
#     def __str__(self):
#         return f'{self.street} {self.country} {str(self.user)}'
