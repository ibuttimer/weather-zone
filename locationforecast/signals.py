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

from forecast import registry_open, Registry
from weather_zone import provider_settings_name

from .constants import THIS_APP, MET_EIREANN, MET_NORWAY_CLASSIC
from .met_eireann import MetEireannProvider
from .met_norway import MetNorwayProvider


# provider to config key mapping
MN_PROVIDER_CFG_KEYS = {
    'friendly_name': 'name',
    'url': 'url',
    'lat_q': 'latitude',
    'lng_q': 'longitude',
    'tz': 'tz',
}
ME_PROVIDER_CFG_KEYS = MN_PROVIDER_CFG_KEYS.copy()
ME_PROVIDER_CFG_KEYS.update({
    'from_q': 'from',
    'to_q': 'to',
})
PROVIDER_NAME = 'name'


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

    print(f"Registry open signal received from {sender}")

    # create Met Eireann provider
    config = settings.FORECAST_APPS_SETTINGS.get(
        provider_settings_name(THIS_APP, MET_EIREANN)
    )
    provider_args = {
        key: config.get(ME_PROVIDER_CFG_KEYS[key])
        for key in ME_PROVIDER_CFG_KEYS
    }
    provider_args[PROVIDER_NAME] = MET_EIREANN

    provider = MetEireannProvider(**provider_args)

    if settings.CACHED_MET_EIREANN_RESULT:
        provider.cached_result = settings.CACHED_MET_EIREANN_RESULT
    registry.add(provider.name, provider)

    print(f"registered: {provider.name} provider")

    # create Met Norway classic provider
    config = settings.FORECAST_APPS_SETTINGS.get(
        provider_settings_name(THIS_APP, MET_NORWAY_CLASSIC)
    )
    provider_args = {
        key: config.get(MN_PROVIDER_CFG_KEYS[key])
        for key in MN_PROVIDER_CFG_KEYS
    }
    provider_args[PROVIDER_NAME] = MET_NORWAY_CLASSIC

    provider = MetNorwayProvider(**provider_args)

    if settings.CACHED_MET_NORWAY_CLASSIC_RESULT:
        provider.cached_result = settings.CACHED_MET_NORWAY_CLASSIC_RESULT
    registry.add(provider.name, provider)

    print(f"registered: {provider.name} provider")
