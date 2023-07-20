"""
Signal processing for met_eireann app
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

from .constants import THIS_APP
from .provider import MetEireannProvider


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

    # create provider
    config = settings.PROVIDER_SETTINGS.get(THIS_APP)
    provider = MetEireannProvider(**{
        'name': THIS_APP,
        'url': config.get('url'),
        'lat_q': config.get('latitude'),
        'long_q': config.get('longitude'),
        'from_q': config.get('from'),
        'to_q': config.get('to')
    })
    registry.add(provider.name, provider)

    print(f"Registry open signal received from {sender}")
    print(f"kwargs: {kwargs}")
    print(f"registry: {registry}")