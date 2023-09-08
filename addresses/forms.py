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
from typing import Type, List

from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries import countries
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from utils import FormMixin # , get_user_model# error_messages, ErrorMsgs,
from .constants import (
    LINE1_FIELD, LINE2_FIELD, CITY_FIELD, STATE_FIELD, POSTCODE_FIELD,
    COUNTRY_FIELD, SET_AS_DEFAULT_FIELD
)


class AddressForm(FormMixin, forms.Form):
    """
    Form for address
    """
    MAX_ADDR_LINE_LEN = 100
    MAX_POSTCODE_LINE_LEN = 10

    LINE1_FIELD = LINE1_FIELD
    LINE2_FIELD = LINE2_FIELD
    CITY_FIELD = CITY_FIELD
    STATE_FIELD = STATE_FIELD
    POSTCODE_FIELD = POSTCODE_FIELD
    COUNTRY_FIELD = COUNTRY_FIELD
    SET_AS_DEFAULT_FIELD = SET_AS_DEFAULT_FIELD

    line1 = forms.CharField(label=_('Line 1'), max_length=MAX_ADDR_LINE_LEN,
                            required=False)
    line2 = forms.CharField(label=_('Line 2'), max_length=MAX_ADDR_LINE_LEN,
                            required=False)
    city = forms.CharField(label=_('City'), max_length=MAX_ADDR_LINE_LEN,
                           required=False)
    state = forms.CharField(label=_('State/Province/Region'),
                            max_length=MAX_ADDR_LINE_LEN, required=False)
    postcode = forms.CharField(
        label=_('Postcode'), max_length=MAX_POSTCODE_LINE_LEN, required=False)
    country = CountryField(blank_label=_("(Select country)"),
                           blank=True).formfield()
    set_as_default = forms.BooleanField(
        label=_("Set as default"), initial=False, required=False)

    _meta_class: Type[object] = None

    @dataclass
    class Meta:
        """ Form metadata """
        addr_fields = [
            # address fields in order of display
            LINE1_FIELD, LINE2_FIELD, CITY_FIELD, STATE_FIELD,
            POSTCODE_FIELD, COUNTRY_FIELD
        ]
        # fields in order of display
        fields = addr_fields.copy()
        fields.extend([
            SET_AS_DEFAULT_FIELD
        ])
        select_fields = [
            COUNTRY_FIELD
        ]
        check_fields = [
            SET_AS_DEFAULT_FIELD
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

        self._do_init(AddressForm.Meta, *args, **kwargs)

    def _do_init(self, meta: Type[object], *args, **kwargs):
        """
        Initialise the form
        :param meta:
        :param args:
        :param kwargs:
        :return:
        """
        self._meta_class = meta

        # add the bootstrap class to the widget
        self.add_form_control(meta.fields,
                              exclude=meta.select_fields + meta.check_fields)
        self.add_form_select(meta.select_fields)
        self.add_form_check_input(meta.check_fields)
        # add autocomplete attributes
        # https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
        self.add_attribute(meta.fields, 'autocomplete', {
            LINE1_FIELD: 'address-line1',
            LINE2_FIELD: 'address-line2',
            CITY_FIELD: 'address-level2',
            STATE_FIELD: 'address-level1',
            POSTCODE_FIELD: 'postal-code',
            COUNTRY_FIELD: 'country'
        })

    def cleaned_addr_field_generator(self):
        """ Generator for cleaned address fields """
        idx = 0
        while idx < len(self._meta_class.addr_fields):
            yield self.cleaned_data.get(self._meta_class.addr_fields[idx])
            idx += 1

    def clean(self):
        """
        Validate the form
        """
        if not self.empty_permitted:
            # check that at least one line is entered
            if not any(self.cleaned_addr_field_generator()):
                raise forms.ValidationError(
                    _("No fields entered"), code="empty")

    def get_field(self, field_name: str) -> str:
        """
        Get field from form converting country code to name
        :param field_name: field name
        :return: field value
        """
        field = self.cleaned_data.get(field_name)
        if field_name == AddressForm.COUNTRY_FIELD and field:
            field = dict(countries)[field]
        return field

    def get_addr_fields_data(self) -> List[str]:
        """
        Get the entered address fields data
        :return: list of data from address fields
        """
        return [
            b for b in map(
                self.get_field, AddressForm.Meta.addr_fields
            ) if b
        ]
