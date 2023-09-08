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
from datetime import datetime
from typing import Callable, List, Optional, Union

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_http_methods
from django_countries import countries

from addresses import ADDRESS_SERVICE
from broker import Broker, ServiceType, ICrudService, ServiceCacheMixin, \
    IService
from weather_warning.constants import COUNTRY_ROUTE_NAME
from weather_zone.constants import (
    WARNING_APP_NAME
)
from base import TITLE_CTX, PAGE_HEADING_CTX, PAGE_SUB_HEADING_CTX
from addresses import (
    USER_FIELD, COUNTRY_FIELD, COMPONENTS_FIELD, FORMATTED_ADDR_FIELD,
    LATITUDE_FIELD, LONGITUDE_FIELD, IS_DEFAULT_FIELD
)
from utils import (
    GET, app_template_path, reverse_q, namespaced_url, Crud,
    redirect_on_success_or_render, html_tag
)

from .constants import (
    THIS_APP, ADDRESS_FORM_CTX, UNAUTH_SKIP_FIELDS_CTX, SUBMIT_URL_CTX,
    SUBMIT_BTN_TEXT_CTX,
    FORECAST_LIST_CTX, FORECAST_CTX, ROW_TYPES_CTX,
    WARNING_LIST_CTX, WARNING_CTX, WARNING_URL_CTX, WARNING_URL_ARIA_CTX,
    ADDRESS_ROUTE_NAME, DISPLAY_ROUTE_NAME, QUERY_TIME_RANGE, QUERY_PROVIDER
)
from .convert import Units, speed_conversion
from .enums import ForecastType, AttribRowTypes
from .forms import AddressForm
from .geocoding import geocode_address
from .dto import (
    GeoAddress, Forecast, AttribRow, ForecastEntry, WeatherWarnings
)
from .misc import RangeArg, DateRange
from .constants import ALL_PROVIDERS
from .registry import Registry


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
    return html_tag('span', tag_content=forecast.provider, **{
        'class': 'span__provider-name'
    })


def measurement_unit_wrapper(fmt: str):
    """"
    Wrapper to add measurement unit to value
    :param fmt: format string for value
    :return: function to add measurement unit to value
    """
    def add_measurement_unit(
            forecast: Forecast, ar: AttribRow, measurement: str,
            index: int, prev_measurement: str) -> str:
        """
        Add unit to measurement
        :param forecast: forecast
        :param ar: AttribRow
        :param measurement: value of measurement
        :return: formatted measurement
        """
        unit = forecast.get_units(ar.attribute)
        if fmt:
            measurement = f'{{0:{fmt}}}'.format(measurement)
        return f'{measurement}{unit}' if unit else measurement

    return add_measurement_unit


def speed_conversion_wrapper(to_unit: Units, fmt: str = None):
    """"
    Wrapper to add value speed conversion
    :param to_unit: unit to convert to
    :param fmt: format string for value
    :return: function to add value speed conversion
    """
    def forecast_speed_conversion(
            forecast: Forecast, ar: AttribRow, measurement: float,
            index: int, prev_measurement: float) -> str:
        """
        Convert speed measurement for forecast display
        :param forecast: Forecast
        :param ar: Attribute row
        :param measurement: forcast measurement
        :return:
        """
        from_unit = Units.from_str(forecast.get_units(ar.attribute))
        measurement = speed_conversion(measurement, from_unit, to_unit)
        return f'{{0:{fmt}}}'.format(measurement) if fmt else measurement

    return forecast_speed_conversion


def forecast_date(forecast: Forecast, ar: AttribRow, value: datetime,
                  index: int, prev_value: datetime) -> str:
    """
    Format the forecast date for display
    :param forecast: forecast
    :param ar: AttribRow
    :param value: value to format
    :param index: index of value
    :param prev_value: previous value
    :return: formatted date
    """
    # only display date if it is different from previous date
    return value.strftime('%a<br>%d %b') \
        if value.date() != (prev_value.date() if prev_value else None) else ''


FULL_DISPLAY_ITEMS = [
    # display text: str or Callable[[Forecast, AttribRow], str]
    # attribute name
    # format function: Callable[[Forecast, AttribRow, Any, int, Any], str]
    #    where;
    #       Forecast is the forecast object
    #       AttribRow is the attribute row object
    #       Any is the value to display
    #       int is the index of the value
    #       Any is the previous value displayed
    # type: AttribRowTypes
    AttribRow(
        add_provider, ForecastEntry.END_KEY, forecast_date,
        AttribRowTypes.HEADER),
    AttribRow(
        '', ForecastEntry.END_KEY,
        lambda f, a, x, i, p: x.strftime('%H:%M'), AttribRowTypes.HEADER),
    AttribRow('', ForecastEntry.ICON_KEY, type=AttribRowTypes.WEATHER_ICON),
    AttribRow(
        title_unit_wrapper(_('Temperature')), ForecastEntry.TEMPERATURE_KEY,
        measurement_unit_wrapper('.0f')),
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
        speed_conversion_wrapper(Units.KPH, fmt='.0f')),
    AttribRow(
        _('Wind Direction'), ForecastEntry.WIND_DIR_ICON_KEY,
        type=AttribRowTypes.WIND_DIR_ICON),
    AttribRow(
        title_unit_wrapper(_('Wind Gust'), unit=Units.KPH),
        ForecastEntry.WIND_GUST_KEY,
        speed_conversion_wrapper(Units.KPH, fmt='.0f')),
]

SUMMARY_DISPLAY_ENTRIES = [
    ForecastEntry.END_KEY, ForecastEntry.ICON_KEY,
    ForecastEntry.TEMPERATURE_KEY, ForecastEntry.PRECIPITATION_KEY
]
SUMMARY_DISPLAY_ITEMS = list(filter(
    lambda x: x.attribute in SUMMARY_DISPLAY_ENTRIES, FULL_DISPLAY_ITEMS
))
SUMMARY_DISPLAY_ITEMS.append(
    AttribRow(
        title_unit_wrapper(_('Wind Speed')),
        ForecastEntry.WIND_SPEED_ICON_KEY, type=AttribRowTypes.WIND_SPEED_ICON)
)

FORECAST_META = {
    # title, template, display_attribs
    ForecastType.LOCATION: (
        _("Location forecast"), "forecast.html", FULL_DISPLAY_ITEMS),
    ForecastType.DEFAULT_ADDR: (
        _("Default address forecast"), "dflt_forecast.html",
        SUMMARY_DISPLAY_ITEMS),
}


def get_display_item_attribute_key(
        display_items: List[AttribRow], filter_fxn: Callable) -> Callable:
    """
    Get display item attribute key for matching filter function
    :param display_items: list of display items
    :param filter_fxn: function to filter display items
    :return: display item type key
    """
    item_list = list(filter(filter_fxn, display_items))
    return None if item_list is None or len(item_list) == 0 else \
        item_list[0].attribute


class ForecastAddress(ServiceCacheMixin, View):
    """
    Class-based view for address forecast
    """

    # _address_service: Optional[ICrudService]
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._address_service = None
    #
    # def address_service(self) -> ICrudService:
    #     """
    #     Get the address service
    #     :return: instance of address service
    #     """
    #     if not self._address_service:
    #         self._address_service = Broker.get_instance().get(
    #             'AddressService', ServiceType.DB_CRUD)
    #     return self._address_service

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

            geo_address, geocode_result = geocode_address(
                form.get_addr_fields_data())
            success = geo_address.is_valid

            if success:
                if request.user.is_authenticated:
                    save_to_profile = form.get_field(
                        AddressForm.SAVE_TO_PROFILE_FIELD)
                    set_as_default = form.get_field(
                        AddressForm.SET_AS_DEFAULT_FIELD)
                else:
                    save_to_profile = False
                    set_as_default = False

                if save_to_profile or set_as_default:
                    # save to profile
                    addr_kwargs = {
                        f'{USER_FIELD}': request.user,
                        f'{LATITUDE_FIELD}': geo_address.lat,
                        f'{LONGITUDE_FIELD}': geo_address.lng,
                    }

                    address_service: Union[IService, ICrudService] = \
                        self.service(ADDRESS_SERVICE, stype=ServiceType.DB_CRUD)

                    addr = address_service.get(**addr_kwargs)
                    if addr is None:
                        # add new address
                        addr = address_service.create(
                            request.user, geocode_result)
                    else:
                        # update existing address
                        if set_as_default != addr.is_default:
                            addr_kwargs['update'] = {
                                f'{IS_DEFAULT_FIELD}': set_as_default
                            }
                            updated = address_service.update(
                                **addr_kwargs)

            # need to redirect to url with query parameters
            query_kwargs = geo_address.as_dict()
            query_kwargs[QUERY_TIME_RANGE] = form.get_field(
                AddressForm.TIME_RANGE_FIELD)
            query_kwargs[QUERY_PROVIDER] = form.get_field(
                AddressForm.PROVIDER_FIELD)
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
            UNAUTH_SKIP_FIELDS_CTX: [
                AddressForm.SAVE_TO_PROFILE_FIELD,
                AddressForm.SET_AS_DEFAULT_FIELD
            ],
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

    provider = request.GET.get(QUERY_PROVIDER, None)    # default is all

    return _display_forecast(request, geo_address, ForecastType.LOCATION,
                             dates, provider, *args, **kwargs)


def _display_forecast(request: HttpRequest, geo_address: GeoAddress,
                      forecast_type: ForecastType, dates: DateRange,
                      provider: str, *args, **kwargs) -> HttpResponse:
    """
    Get forecast view function
    :param request: http request
    :param geo_address: GeoAddress
    :param forecast_type: ForecastType enum
    :param dates: DateRange
    :param provider: name of forecast provider
    :param args: additional arbitrary arguments
    :param kwargs: additional keyword arguments
    :return: http response
    """
    if provider and provider.lower() == ALL_PROVIDERS:
        provider = None    # default is all

    _, _, display_attribs = FORECAST_META.get(forecast_type)

    forecast_kwargs = {}
    for row_type in AttribRowTypes.icon_types():
        key = get_display_item_attribute_key(
            display_attribs, lambda ar: ar.type == row_type)
        if key:
            forecast_kwargs[row_type.value] = key

    registry = Registry.get_instance()

    forecasts = registry.generate_forecast(
        geo_address, provider=provider,
        start=dates.start, end=dates.end, **forecast_kwargs)

    warnings = registry.generate_warnings(geo_address.country,
                                          provider=provider)

    template_path, context = forecast_render_info(forecast_type, forecasts,
                                                  warnings)

    return render(request, template_path, context=context)


@require_http_methods([GET])
def display_home(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    """
    Get home view function
    :param request: http request
    :param args: additional arbitrary arguments
    :param kwargs: additional keyword arguments
    :return: http response
    """

    addr_service: ICrudService = Broker.get_instance().get(
        'AddressService', ServiceType.DB_CRUD)

    addr = addr_service.get(user=request.user, is_default=True)

    geo_address = GeoAddress.from_address(addr)

    return _display_forecast(request, geo_address, ForecastType.DEFAULT_ADDR,
                             RangeArg.TODAY.as_dates(), None,
                             *args, **kwargs)



def forecast_render_info(forecast_type: ForecastType, forecasts: List[Forecast],
                         warnings: List[WeatherWarnings]):
    """
    Get info to render a list of forecasts
    :param forecast_type: ForecastType enum
    :param forecasts: Forecast list
    :param warnings: WeatherWarnings list
    :return: tuple of template path and context
    """
    formatted_addr = None
    country_code = None

    title, template, display_attribs = FORECAST_META.get(forecast_type)

    # generate list of forecasts
    forecast_list = []
    for forecast in forecasts:
        # filter display items to only those available in forecast
        display_items = list(filter(
            lambda x: x.attribute in forecast.forecast_attribs,
            display_attribs
        ))
        # transform forecast entries into a list of attribute lists
        forecast.set_attrib_series(display_items)

        forecast_list.append({
            FORECAST_CTX: forecast,
            ROW_TYPES_CTX: list(map(
                lambda x: x.type.value if x.type else x.type, display_items))
        })

        if not formatted_addr:
            formatted_addr = forecast.address.formatted_address
            country_code = forecast.address.country

    # generate list of warnings
    warning_list = []
    for warning in warnings:
        warning_list.append({
            WARNING_CTX: warning,
            WARNING_URL_CTX: reverse_q(
                namespaced_url(WARNING_APP_NAME, COUNTRY_ROUTE_NAME),
                args=[country_code], query_kwargs={
                    QUERY_PROVIDER: warning.provider_id
                }
            ),
            WARNING_URL_ARIA_CTX: _("view %(provider)s weather warnings.") % {
                "provider": warning.provider
            }
        })

    context = {
        TITLE_CTX: title,
        PAGE_HEADING_CTX: title,
        PAGE_SUB_HEADING_CTX: formatted_addr,
        FORECAST_LIST_CTX: forecast_list,
        WARNING_LIST_CTX: warning_list
    }

    return app_template_path(THIS_APP, template), context
