"""
Provider loading
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
from typing import List, Callable

from django.conf import settings

from weather_zone import provider_settings_name

from .provider import Provider
from .registry import Registry

ID_CAMEL_CAPITAL = re.compile(r'_([a-zA-Z]){1}')


def load_provider(registry: Registry, provider_list: List[str], app_name: str,
                  app_settings_key: str, provider_cfg_keys: dict,
                  finish_cfg: Callable[[Provider], None] = None):
    """
    Load a provider

    :param registry: provider registry
    :param provider_list: list of providers to load
    :param app_name: app name
    :param app_settings_key: key to app settings in django settings
    :param provider_cfg_keys: map of provider config keys to setting attribute
                            names
    :param finish_cfg: additional configuration function; default None
    """
    for app_provider in provider_list:
        # convention is `<provider app name>_<provider id>`
        provider_id = app_provider[len(app_name) + 1:]
        provider_classname = get_provider_classname(
            app_provider[len(app_name):])

        # create provider instance
        app_settings = getattr(settings, app_settings_key, {})
        config = app_settings.get(
            provider_settings_name(app_name, provider_id)
        )
        provider_args = {
            k: v for k, v in [
                (key, config.get(provider_cfg_keys[key], None))
                for key in provider_cfg_keys
            ] if v is not None
        }
        provider_args[Provider.NAME_PROP] = provider_id

        # instantiate provider
        provider = get_class(
            f'{app_name}.{provider_id}', provider_classname)(**provider_args)

        # additional configuration
        if finish_cfg:
            finish_cfg(provider)

        registry.add(provider.name, provider)

        print(f"registered provider: {provider}")


def get_provider_classname(provider_id: str, ending: str = 'Provider'):
    """
    Convert provider id to class name;
    e.g. '_open_weather' -> 'OpenWeatherProvider'

    :param provider_id: provider id
    :param ending: class name ending; default 'Provider'
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

    return f'{provider_id}{ending}'


def get_class(module_name: str, class_name: str):
    """
    Get class from module
    :param module_name: path of module
    :param class_name: name of class
    :return:
    """
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
