"""
This file is used to create the views for the forecast app.
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
from collections import namedtuple

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_http_methods
from django_countries import countries

from weather_zone.constants import (
    LOCATIONFORECAST_APP_NAME
)
from utils import (
    GET, app_template_path, reverse_q, namespaced_url, Crud,
    redirect_on_success_or_render,
)

from .constants import (
    THIS_APP, ADDRESS_FORM_CTX, SUBMIT_URL_CTX, ADDRESS_ROUTE_NAME,
    SUBMIT_BTN_TEXT_CTX, TITLE_CTX, PAGE_HEADING_CTX,
    FORECAST_CTX, ROW_TYPES_CTX, DISPLAY_ROUTE_NAME, QUERY_TIME_RANGE,
    PAGE_SUB_HEADING_CTX
)
from .convert import Units, speed_conversion
from .forecast import generate_forecast
from .forms import AddressForm
from .geocoding import geocode_address
from .dto import (
    GeoAddress, Forecast, AttribRow, ForecastEntry, TYPE_WEATHER_ICON,
    TYPE_HDR, TYPE_WIND_DIR_ICON)
from .misc import RangeArg


def title_unit_wrapper(title: str, unit: Units = None):
    """"
    Wrapper to add unit to title
    :param title: title
    :param unit: unit to display; default is forecast unit
    :return: function to add unit to title
    """
    def add_title_unit(forecast: Forecast, ar: AttribRow):
        """
        Add unit to title
        :param forecast: forecast
        :param ar: AttribRow
        :return: title
        """
        unit_symbol = unit.value if unit else forecast.get_units(ar.attribute)
        return f'{title}<br>({unit_symbol})' if unit_symbol else title

    return add_title_unit


def add_provider(forecast: Forecast, ar: AttribRow):
    """
    Add provider to title
    :param forecast: forecast
    :param ar: AttribRow
    :return: title
    """
    return forecast.provider


def measurement_unit_wrapper(format: str):
    """"
    Wrapper to add measurement unit to value
    :param format: format string for value
    :return: function to add measurement unit to value
    """
    def add_measurement_unit(forecast: Forecast, ar: AttribRow, measurement: str):
        """
        Add unit to measurement
        :param forecast: forecast
        :param ar: AttribRow
        :param measurement: measurement
        :return: measurement
        """
        unit = forecast.get_units(ar.attribute)
        if format:
            measurement = f'{{0:{format}}}'.format(measurement)
        return f'{measurement}{unit}' if unit else measurement

    return add_measurement_unit


def speed_conversion_wrapper(to_unit: Units, format: str = None):
    """"
    Wrapper to add value speed conversion
    :param to_unit: unit to convert to
    :param format: format string for value
    :return: function to add value speed conversion
    """
    def forecast_speed_conversion(
            forecast: Forecast, ar: AttribRow, measurement: float):
        """
        Convert speed measurement for forecast display
        :param forecast: Forecast
        :param ar: Attribute row
        :param measurement: forcast measurement
        :return:
        """
        from_unit = Units.from_str(forecast.get_units(ar.attribute))
        measurement = speed_conversion(measurement, from_unit, to_unit)
        return f'{{0:{format}}}'.format(measurement) if format else measurement

    return forecast_speed_conversion


DISPLAY_ITEMS = [
    # display text: str or Callable[[Forecast, AttribRow], str]
    # attribute name
    # format function: Callable[[Forecast, AttribRow, str], str]
    # type
    AttribRow(
        add_provider, ForecastEntry.START_KEY,
        lambda f, a, x: x.strftime('%a<br>%d %b'), TYPE_HDR),
    AttribRow(
        '', ForecastEntry.START_KEY,
        lambda f, a, x: x.strftime('%H:%M'), 'hdr'),
    AttribRow('', ForecastEntry.ICON_KEY, type=TYPE_WEATHER_ICON),
    AttribRow(
        title_unit_wrapper(_('Temperature')), ForecastEntry.TEMPERATURE_KEY),
    AttribRow(
        title_unit_wrapper(_('Precipitation')),
        ForecastEntry.PRECIPITATION_KEY),
    AttribRow(
        _('Precipitation Probability'), ForecastEntry.PRECIPITATION_PROB_KEY,
        measurement_unit_wrapper('.0f')),
    AttribRow(_('Humidity'), ForecastEntry.HUMIDITY_KEY,
              measurement_unit_wrapper('.1f')),
    AttribRow(
        title_unit_wrapper(_('Wind Speed'), unit=Units.KPH),
        ForecastEntry.WIND_SPEED_KEY,
        speed_conversion_wrapper(Units.KPH, format='.0f')),
    AttribRow(
        _('Wind Direction'), ForecastEntry.WIND_DIR_ICON_KEY,
        type=TYPE_WIND_DIR_ICON),
    AttribRow(
        title_unit_wrapper(_('Wind Gust'), unit=Units.KPH),
        ForecastEntry.WIND_GUST_KEY,
        speed_conversion_wrapper(Units.KPH, format='.0f')),
]

class ForecastAddress(View):
    """
    Class-based view for address forecast
    """

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        GET method for Address
        :param request: http request
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """
        template_path, context = self.address_render_info(AddressForm())

        return render(request, template_path, context=context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        POST method to update Opinion
        :param request: http request
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """
        form = AddressForm(data=request.POST)

        form.full_clean()

        success = False
        url = None
        if form.is_valid():
            def get_field(field_name: str) -> str:
                """ Get field from form converting country code to name """
                field = form.cleaned_data.get(field_name)
                if field_name == AddressForm.COUNTRY_FIELD and field:
                    field = dict(countries)[field]
                return field

            geo_address: GeoAddress = geocode_address([
                b for b in map(
                    get_field, AddressForm.Meta.addr_fields
                ) if b
            ])
            success = geo_address.is_valid

            # need to redirect to url with query parameters
            query_kwargs = geo_address.as_dict()
            query_kwargs[QUERY_TIME_RANGE] = get_field(
                AddressForm.TIME_RANGE_FIELD)
            url = reverse_q(
                namespaced_url(THIS_APP, DISPLAY_ROUTE_NAME),
                query_kwargs=query_kwargs
            )

            template_path, context = (None, None)
        else:
            success = False
            template_path, context = self.address_render_info(form)

        return redirect_on_success_or_render(
            request, success,
            redirect_to=url,
            *args, template_path=template_path, context=context,
            **kwargs
        )

    def address_render_info(self, form: AddressForm):
        """
        Get info to render an address form
        :param form: form to use
        :return: tuple of template path and context
        """
        context = {
            TITLE_CTX: _("Forecast location"),
            PAGE_HEADING_CTX: _("Address of forecast location"),
            SUBMIT_BTN_TEXT_CTX: _("Submit"),
            ADDRESS_FORM_CTX: form,
            SUBMIT_URL_CTX: self.url()
        }

        return app_template_path(THIS_APP, "address_form.html"), context

    def url(self) -> str:
        """
        Get url for address input
        :return: url
        """
        return reverse_q(
            namespaced_url(THIS_APP, ADDRESS_ROUTE_NAME)
        )


@require_http_methods([GET])
def display_forecast(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    """
    Get forecast view function
    :param request: http request
    :param args: additional arbitrary arguments
    :param kwargs: additional keyword arguments
    :return: http response
    """
    for query in [
        'formatted_address', 'lat', 'lng', 'is_valid'   # attrib of GeoAddress
    ]:
        if query not in request.GET.dict():
            raise ValueError(f"Missing query parameter {query}")

    geo_address = GeoAddress.from_dict(request.GET.dict())

    time_rng = RangeArg.from_str(
        request.GET.get(QUERY_TIME_RANGE, RangeArg.ALL.value)
    )
    dates = time_rng.as_dates()

    forecast = generate_forecast(geo_address,
                                 provider=LOCATIONFORECAST_APP_NAME,
                                 start=dates.start, end=dates.end)

    template_path, context = forecast_render_info(forecast)

    return render(request, template_path, context=context)


def forecast_render_info(forecast: Forecast):
    """
    Get info to render a forecast
    :param forecast: Forecast
    :return: tuple of template path and context
    """
    # transform forecast entries into a list of attribute lists
    forecast.set_attrib_series(DISPLAY_ITEMS)

    title = _("Location forecast")
    context = {
        TITLE_CTX: title,
        PAGE_HEADING_CTX: title,
        PAGE_SUB_HEADING_CTX: forecast.address.formatted_address,
        FORECAST_CTX: forecast,
        ROW_TYPES_CTX: list(map(lambda x: x.type, DISPLAY_ITEMS))
    }

    return app_template_path(THIS_APP, "forecast.html"), context

