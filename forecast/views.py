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

from utils import (
    GET, app_template_path, reverse_q, namespaced_url, Crud,
    redirect_on_success_or_render,
)

from .constants import (
    THIS_APP, ADDRESS_FORM_CTX, SUBMIT_URL_CTX, ADDRESS_ROUTE_NAME,
    SUBMIT_BTN_TEXT_CTX, TITLE_CTX, PAGE_HEADING_CTX,
    FORECAST_CTX, ROW_TYPES_CTX, DISPLAY_ROUTE_NAME, QUERY_TIME_RANGE
)
from .forecast import generate_forecast
from .forms import AddressForm
from .geocoding import geocode_address
from .dto import GeoAddress, Forecast, AttribRow, ForecastEntry
from .misc import RangeArg


DISPLAY_ITEMS = [
    AttribRow(
        '', ForecastEntry.START_KEY, lambda x: x.strftime('%a<br>%d %b'), 'hdr'),
    AttribRow(
        '', ForecastEntry.START_KEY, lambda x: x.strftime('%H:%M'), 'hdr'),
    AttribRow('', ForecastEntry.ICON_KEY, type='img'),
    AttribRow('Temperature', ForecastEntry.TEMPERATURE_KEY),
    AttribRow('Precipitation', ForecastEntry.PRECIPITATION_KEY),
    AttribRow(
        'Precipitation Probability', ForecastEntry.PRECIPITATION_PROB_KEY),
    AttribRow('Humidity', ForecastEntry.HUMIDITY_KEY),
    AttribRow('Wind Speed', ForecastEntry.WIND_SPEED_KEY),
    AttribRow('Wind Direction', ForecastEntry.WIND_DIR_KEY),
    AttribRow('Wind Gust', ForecastEntry.WIND_GUST_KEY),
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

    forecast = generate_forecast(geo_address, provider='met_eireann',
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
        FORECAST_CTX: forecast,
        ROW_TYPES_CTX: list(map(lambda x: x.type, DISPLAY_ITEMS))
    }

    return app_template_path(THIS_APP, "forecast.html"), context

