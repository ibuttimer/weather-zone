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

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from utils import FormMixin

from broker import ServiceType
from .misc import RangeArg, get_range_choices, get_provider_choices


LINE1_FIELD = 'line1'
LINE2_FIELD = 'line2'
CITY_FIELD = 'city'
LINE4_FIELD = 'state'
POSTCODE_FIELD = 'postcode'
COUNTRY_FIELD = 'country'
TIME_RANGE_FIELD = 'time_range'
PROVIDER_FIELD = 'provider'
SAVE_TO_PROFILE_FIELD = "save_to_profile"
SET_AS_DEFAULT_FIELD = "set_as_default"


class AddressForm(FormMixin, forms.Form):
    """
    Form for address forecast
    """
    MAX_ADDR_LINE_LEN = 100
    MAX_POSTCODE_LINE_LEN = 10

    LINE1_FIELD = LINE1_FIELD
    LINE2_FIELD = LINE2_FIELD
    CITY_FIELD = CITY_FIELD
    LINE4_FIELD = LINE4_FIELD
    POSTCODE_FIELD = POSTCODE_FIELD
    COUNTRY_FIELD = COUNTRY_FIELD
    TIME_RANGE_FIELD = TIME_RANGE_FIELD
    PROVIDER_FIELD = PROVIDER_FIELD
    SAVE_TO_PROFILE_FIELD = SAVE_TO_PROFILE_FIELD
    SET_AS_DEFAULT_FIELD = SET_AS_DEFAULT_FIELD

    line1 = forms.CharField(label=_('Line 1'), max_length=MAX_ADDR_LINE_LEN,
                            required=False)
    line2 = forms.CharField(label=_('Line 2'), max_length=MAX_ADDR_LINE_LEN,
                            required=False)
    city = forms.CharField(label=_('City'), max_length=MAX_ADDR_LINE_LEN,
                           required=False)
    state = forms.CharField(label=_('State/Province/Region'),
                            max_length=MAX_ADDR_LINE_LEN, required=False)
    postcode = forms.CharField(label=_('Postcode'), max_length=10,
                               required=False)
    country = CountryField(blank_label=_("(Select country)"),
                           blank=True).formfield()
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
    set_as_default = forms.BooleanField(
        label=_("Set as default"), initial=False, required=False)

    @dataclass
    class Meta:
        """ Form metadata """
        addr_fields = [
            # address fields in order of display
            LINE1_FIELD, LINE2_FIELD, CITY_FIELD, LINE4_FIELD,
            POSTCODE_FIELD, COUNTRY_FIELD
        ]
        # fields in order of display
        fields = addr_fields.copy()
        fields.extend([
            TIME_RANGE_FIELD, PROVIDER_FIELD, SAVE_TO_PROFILE_FIELD,
            SET_AS_DEFAULT_FIELD
        ])
        select_fields = [
            COUNTRY_FIELD, TIME_RANGE_FIELD, PROVIDER_FIELD
        ]
        check_fields = [
            SAVE_TO_PROFILE_FIELD, SET_AS_DEFAULT_FIELD
        ]
        widgets = {
            # https://pypi.org/project/django-countries/#countryselectwidget
            COUNTRY_FIELD: CountrySelectWidget(
                layout='{widget}<img class="img__country-select-flag" '
                       'id="{flag_id}" src="{country.flag}">'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add the bootstrap class to the widget
        self.add_form_control(
            AddressForm.Meta.fields,
            exclude=
            AddressForm.Meta.select_fields + AddressForm.Meta.check_fields)
        self.add_form_select(AddressForm.Meta.select_fields)
        self.add_form_check_input(AddressForm.Meta.check_fields)
        # add autocomplete attributes
        # https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
        self.add_attribute(AddressForm.Meta.fields, 'autocomplete', {
            LINE1_FIELD: 'address-line1',
            LINE2_FIELD: 'address-line2',
            CITY_FIELD: 'address-level2',
            LINE4_FIELD: 'address-level1',
            POSTCODE_FIELD: 'postal-code',
            COUNTRY_FIELD: 'country'
        })

    def clean(self):
        """
        Validate the form
        :return:
        """
        if not self.empty_permitted:
            # check that at least one line is entered
            if not any(
                [self.cleaned_data.get(f) for f in AddressForm.Meta.fields]
            ):
                raise forms.ValidationError(
                    _("No fields entered"), code="empty")
