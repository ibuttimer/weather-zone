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

from allauth.account import app_settings
from django import forms
from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import (
    SignupForm, LoginForm, PasswordField, AddEmailForm, ResetPasswordForm,
    ChangePasswordForm
)
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth.models import Group

from utils import FormMixin # , get_user_model# error_messages, ErrorMsgs,
from .models import User
from .constants import (
    FIRST_NAME, LAST_NAME, EMAIL, EMAIL_CONFIRM, USERNAME,
    PASSWORD, PASSWORD_CONFIRM, OLD_PASSWORD
)


class UserSignupForm(FormMixin, SignupForm):
    """ Custom user sign up form """

    FIRST_NAME_FF = FIRST_NAME
    LAST_NAME_FF = LAST_NAME
    EMAIL_FF = EMAIL
    EMAIL_CONFIRM_FF = EMAIL_CONFIRM
    USERNAME_FF = USERNAME
    PASSWORD_FF = PASSWORD
    PASSWORD_CONFIRM_FF = PASSWORD_CONFIRM

    @dataclass
    class Meta:
        """ Form metadata """
        model = User
        fields = [
            FIRST_NAME, LAST_NAME, EMAIL, EMAIL_CONFIRM, USERNAME,
            PASSWORD, PASSWORD_CONFIRM
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[UserSignupForm.PASSWORD_FF] = PasswordField(
            label=_("Password"), autocomplete="new-password",
            min_length=settings.MIN_PASSWORD_LEN
        )
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields[UserSignupForm.PASSWORD_CONFIRM_FF] = PasswordField(
                label=_("Confirm password"), autocomplete="new-password",
                min_length=settings.MIN_PASSWORD_LEN
            )

        # add first & last name fields
        self.fields[UserSignupForm.FIRST_NAME_FF] = forms.CharField(
            label=_("First name"),
            max_length=User.USER_ATTRIB_FIRST_NAME_MAX_LEN,
            widget=forms.TextInput(attrs={
                "placeholder": _("User first name")
            }),
        )
        self.fields[UserSignupForm.LAST_NAME_FF] = forms.CharField(
            label=_("Last name"),
            max_length=User.USER_ATTRIB_LAST_NAME_MAX_LEN,
            widget=forms.TextInput(attrs={
                "placeholder": _("User last name")
            }),
        )

        # reorder fields so first & last name appear at start
        self.fields.move_to_end(UserSignupForm.LAST_NAME_FF, last=False)
        self.fields.move_to_end(UserSignupForm.FIRST_NAME_FF, last=False)

        # add the bootstrap class to the widget
        self.add_form_control(UserSignupForm.Meta.fields)

    def signup(self, request: HttpRequest, user: User) -> None:
        """
        Perform custom signup actions
        :param request:
        :param user: user object
        """
        pass


class UserLoginForm(FormMixin, LoginForm):
    """ Custom user login form """

    LOGIN_FF = "login"
    PASSWORD_FF = "password"

    @dataclass
    class Meta:
        """ Form metadata """
        fields = ["login", "password"]

    password = PasswordField(
        label=_("Password"), autocomplete="current-password",
        min_length=settings.MIN_PASSWORD_LEN
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add the bootstrap class to the widget
        self.add_form_control(UserLoginForm.Meta.fields)


class UserForm(FormMixin, forms.ModelForm):
    """
    Form to update a user.
    """

    FIRST_NAME_FF = FIRST_NAME
    LAST_NAME_FF = LAST_NAME
    EMAIL_FF = EMAIL

    first_name = forms.CharField(
        label=_("First name"),
        max_length=User.USER_ATTRIB_FIRST_NAME_MAX_LEN,
        required=False)
    last_name = forms.CharField(
        label=_("Last name"),
        max_length=User.USER_ATTRIB_LAST_NAME_MAX_LEN,
        required=False)
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("Email address"),
                "autocomplete": "email",
            }
        ),
        required=False,
        disabled=True
    )

    @dataclass
    class Meta:
        """ Form metadata """
        model = User
        fields = [
            FIRST_NAME, LAST_NAME, EMAIL
        ]
        non_bootstrap_fields = []
        help_texts = {
            FIRST_NAME: 'User first name.',
            LAST_NAME: 'User last name.',
            EMAIL: 'Email address of user.',
        }
        # error_messages = error_messages(
        #     model.model_name_caps(),
        #     *[ErrorMsgs(field, max_length=max_len)
        #       for field, max_len in [
        #           (FIRST_NAME, User.USER_ATTRIB_FIRST_NAME_MAX_LEN),
        #           (LAST_NAME, User.USER_ATTRIB_LAST_NAME_MAX_LEN)
        #       ]]
        # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add the bootstrap class to the widget
        self.add_form_control(
            UserForm.Meta.fields, exclude=UserForm.Meta.non_bootstrap_fields)


class UserResetPasswordForm(FormMixin, ResetPasswordForm):
    """ Custom user password reset form """

    EMAIL_FF = EMAIL

    @dataclass
    class Meta:
        """ Form metadata """
        fields = [EMAIL]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add the bootstrap class to the widget
        self.add_form_control(UserResetPasswordForm.Meta.fields)


class UserChangePasswordForm(FormMixin, ChangePasswordForm):
    """ Custom user password change form """

    OLD_PASSWORD_FF = OLD_PASSWORD
    PASSWORD_FF = PASSWORD
    PASSWORD_CONFIRM_FF = PASSWORD_CONFIRM

    @dataclass
    class Meta:
        """ Form metadata """
        fields = [OLD_PASSWORD, PASSWORD, PASSWORD_CONFIRM]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add the bootstrap class to the widget
        self.add_form_control(UserChangePasswordForm.Meta.fields)


class UserAddEmailForm(FormMixin, AddEmailForm):
    """ Custom user add email form """

    EMAIL_FF = EMAIL

    @dataclass
    class Meta:
        """ Form metadata """
        fields = [EMAIL]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add the bootstrap class to the widget
        self.add_form_control(UserAddEmailForm.Meta.fields)


class UserSocialSignupForm(FormMixin, SocialSignupForm):
    """ Custom user social sign up form """

    EMAIL_FF = EMAIL
    EMAIL_CONFIRM_FF = EMAIL_CONFIRM
    USERNAME_FF = USERNAME

    @dataclass
    class Meta:
        """ Form metadata """
        fields = [
            EMAIL, EMAIL_CONFIRM, USERNAME
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add the bootstrap class to the widget
        self.add_form_control(UserSocialSignupForm.Meta.fields)
