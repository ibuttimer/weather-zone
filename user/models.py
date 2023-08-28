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
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from utils import ModelMixin

from .constants import (
    FIRST_NAME, LAST_NAME, PREVIOUS_LOGIN,
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


class CompressedJsonTextField(models.BinaryField):
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
        json_str = json.dumps(super().pre_save(model_instance, add))
        byte_data = zlib.compress(json_str.encode())
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
            value = json.loads(zlib.decompress(value).decode())
        return value

    def to_python(self, value):
        # If it's a string, it should be base64-encoded data
        return json.loads(zlib.decompress(value).decode())
