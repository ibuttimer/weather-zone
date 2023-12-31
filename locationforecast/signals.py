"""
Signal processing for locationforecast app
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
from django.conf import settings
from django.dispatch import receiver

from forecast import (
    registry_open, Registry, load_provider, Provider, ProviderCfgEntry
)

from .constants import THIS_APP
from .provider import LocationforecastProvider
from .met_eireann_forecast import MetEireannForecastProvider


# map of all possible provider config keys (excluding Provider.NAME_PROP)
# to the keys used in the settings
PROVIDER_CFG_KEYS = {
    Provider.FRIENDLY_NAME_PROP: ProviderCfgEntry('name'),
    Provider.URL_PROP: ProviderCfgEntry('url'),
    Provider.DATA_URL_PROP: ProviderCfgEntry('data_url'),
    LocationforecastProvider.LATITUDE_PROP: ProviderCfgEntry('latitude'),
    LocationforecastProvider.LONGITUDE_PROP: ProviderCfgEntry('longitude'),
    MetEireannForecastProvider.FROM_PROP: ProviderCfgEntry('from'),
    MetEireannForecastProvider.TO_PROP: ProviderCfgEntry('to'),
    Provider.TZ_PROP: ProviderCfgEntry('tz'),
    Provider.COUNTRY_PROP: ProviderCfgEntry('country', lambda x: x.split(',')),
}


@receiver(registry_open)
def registry_open_handler(sender, **kwargs):
    """
    Handler for registry open signal
    :param sender: sender which sent the signal
    :param kwargs: keyword arguments including
        registry: registry that was opened
    :return:
    """
    registry: Registry = kwargs.get('registry')

    print(f"{THIS_APP}: Registry open signal received from {str(registry)}")

    def finalise_config(provider: Provider):
        cached_result_setting = f'CACHED_{provider.name.upper()}_RESULT'
        cached_result = getattr(settings, cached_result_setting, None)
        if cached_result:
            provider.cached_result = cached_result

    load_provider(registry, settings.FORECAST_PROVIDERS, THIS_APP,
                  'FORECAST_APPS_SETTINGS', PROVIDER_CFG_KEYS,
                  finish_cfg=finalise_config)
