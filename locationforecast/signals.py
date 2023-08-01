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
import importlib
import re

from django.conf import settings
from django.dispatch import receiver

from forecast import registry_open, Registry
from weather_zone import provider_settings_name

from .constants import THIS_APP


PROVIDER_CFG_KEYS = {
    'friendly_name': 'name',
    'url': 'url',
    'lat_q': 'latitude',
    'lng_q': 'longitude',
    'from_q': 'from',
    'to_q': 'to',
    'tz': 'tz',
}

PROVIDER_NAME = 'name'

ID_CAMEL_CAPITAL = re.compile(r'_([a-zA-Z]){1}')


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

    # FORECAST_PROVIDERS=locationforecast_met_eireann,locationforecast_met_norway_classic
    for app_provider in settings.FORECAST_PROVIDERS:
        # convention is `<provider app name>_<provider id>`
        provider_id = app_provider[len(THIS_APP) + 1:]
        provider_classname = get_provider_classname(
            app_provider[len(THIS_APP):])

        # create provider instance
        config = settings.FORECAST_APPS_SETTINGS.get(
            provider_settings_name(THIS_APP, provider_id)
        )
        provider_args = {
            k: v for k, v in [
                (key, config.get(PROVIDER_CFG_KEYS[key], None)) for key in PROVIDER_CFG_KEYS
            ] if v is not None
        }
        provider_args[PROVIDER_NAME] = provider_id

        # instantiate provider
        provider = get_class(
            f'{THIS_APP}.{provider_id}', provider_classname)(**provider_args)

        cached_result_setting = f'CACHED_{provider_id.upper()}_RESULT'
        cached_result = getattr(settings, cached_result_setting, None)
        if cached_result:
            provider.cached_result = cached_result
        registry.add(provider.name, provider)

        print(f"registered: {provider.name} provider")


def get_provider_classname(provider_id: str):
    """
    Convert provider id to class name
    :param provider_id:
    :return: classname of provider
    """
    idx = 0
    match = True
    while match:
        match = ID_CAMEL_CAPITAL.search(provider_id, idx)
        if match:
            idx = match.start()
            replacement = match.group(1).upper()
            provider_id = f"{provider_id[:idx]}{replacement}" \
                          f"{provider_id[match.end():]}"
            idx += len(replacement)

    return f'{provider_id}Provider'


def get_class(module_name: str, class_name: str):
    """
    Get class from module
    :param module_name: path of module
    :param class_name: name of class
    :return:
    """
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
