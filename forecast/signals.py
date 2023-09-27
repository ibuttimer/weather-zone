"""
Signal processing for forecast app
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
import django.dispatch
from django.dispatch import receiver

from broker import broker_open, Broker, ServiceType

from .constants import THIS_APP
from .services import GeocodeService
from .registry import Registry


# Signal sent when the registry is opened
registry_open = django.dispatch.Signal()


@receiver(broker_open)
def broker_open_handler(sender, **kwargs):
    """
    Handler for broker open signal
    :param sender: sender which sent the signal
    :param kwargs: keyword arguments including
        registry: registry that was opened
    :return:
    """
    broker: Broker = kwargs.get('broker')

    print(f"{THIS_APP}: Broker open signal received from {str(broker)}")

    # register services
    broker.add(GeocodeService.__name__, ServiceType.SERVICE,
               GeocodeService.get_instance())

    # create the registry instance
    registry = Registry.get_instance()
    # send the registry_open signal
    registry_open.send(sender=registry.__class__, registry=registry)
