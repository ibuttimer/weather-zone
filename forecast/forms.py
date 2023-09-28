"""
Forecast forms
"""
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
from dataclasses import dataclass

from django import forms
from django.utils.translation import gettext_lazy as _

from addresses.constants import SET_AS_DEFAULT_FIELD
from addresses.forms import AddressForm as BaseAddressForm

from broker import ServiceType
from .misc import get_range_choices, get_provider_choices


TIME_RANGE_FIELD = 'time_range'
PROVIDER_FIELD = 'provider'
SAVE_TO_PROFILE_FIELD = "save_to_profile"


class AddressForm(BaseAddressForm):
    """
    Form for address forecast
    """
    TIME_RANGE_FIELD = TIME_RANGE_FIELD
    PROVIDER_FIELD = PROVIDER_FIELD
    SAVE_TO_PROFILE_FIELD = SAVE_TO_PROFILE_FIELD

    # choices set during init
    time_range = forms.ChoiceField(
        label=_("Time range"), required=True, choices=get_range_choices())
    # choices set during init
    provider = forms.ChoiceField(
        label=_("Provider"), required=True, choices=get_provider_choices(
            stype=ServiceType.FORECAST
        ))
    save_to_profile = forms.BooleanField(
        label=_("Save to profile"), initial=False, required=False)

    @dataclass
    class Meta(BaseAddressForm.Meta):
        """ Form metadata """
        # fields in order of display
        fields = BaseAddressForm.Meta.addr_fields.copy()
        fields.extend([
            TIME_RANGE_FIELD, PROVIDER_FIELD, SAVE_TO_PROFILE_FIELD,
            SET_AS_DEFAULT_FIELD
        ])
        select_fields = BaseAddressForm.Meta.select_fields.copy()
        select_fields.extend([
            TIME_RANGE_FIELD, PROVIDER_FIELD
        ])
        check_fields = BaseAddressForm.Meta.check_fields.copy()
        check_fields.extend([
            SAVE_TO_PROFILE_FIELD
        ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._do_init(AddressForm.Meta, *args, **kwargs)

        # reorder fields so set_as_default appears at end
        self.fields[SET_AS_DEFAULT_FIELD] = self.fields.pop(SET_AS_DEFAULT_FIELD)

    def clean(self):
        """
        Validate the form
        :return:
        """
        if not self.empty_permitted:
            # check that at least one basic address line is entered
            if not any(self.cleaned_data.get(f)
                       for f in BaseAddressForm.Meta.fields):
                raise forms.ValidationError(
                    _("No fields entered"), code="empty")
