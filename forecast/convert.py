"""
Convert data to a format suitable for forecast
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
from enum import Enum, auto


class Units(Enum):
    """
    Measurement units
    """
    MPS = 'm/s'
    KPH = 'km/h'
    KNOTS = 'kn'
    MPH = 'mph'

    @classmethod
    def from_str(cls, unit: str) -> 'Units':
        """
        Get a Units enum from a string
        :param unit: unit string
        :return: Units enum
        """
        for enum in cls:
            if enum.value == unit:
                return enum
        raise ValueError(f'Unknown unit: {unit}')


_CONVERTERS = {
    Units.MPS: {
        Units.MPS: lambda x: x,
        Units.KPH: lambda x: x * 3.6,
        Units.KNOTS: lambda x: x * 1.94384,
        Units.MPH: lambda x: x * 2.23694,
    },
    Units.KPH: {
        Units.MPS: lambda x: x / 3.6,
        Units.KPH: lambda x: x,
        Units.KNOTS: lambda x: x * 0.539957,
        Units.MPH: lambda x: x * 0.621371,
    },
    Units.KNOTS: {
        Units.MPS: lambda x: x / 1.94384,
        Units.KPH: lambda x: x / 0.539957,
        Units.KNOTS: lambda x: x,
        Units.MPH: lambda x: x * 1.15078,
    },
    Units.MPH: {
        Units.MPS: lambda x: x / 2.23694,
        Units.KPH: lambda x: x / 0.621371,
        Units.KNOTS: lambda x: x / 1.15078,
        Units.MPH: lambda x: x,
    },
}

def speed_conversion(value: float, from_unit: Units, to_unit: Units) -> float:
    """
    Convert speed between units
    :param value: speed value
    :param from_unit: from unit
    :param to_unit: to unit
    :return: converted speed
    """
    if from_unit not in _CONVERTERS or to_unit not in _CONVERTERS[from_unit]:
        raise ValueError(f'Unknown unit conversion: {from_unit} to {to_unit}')

    return _CONVERTERS[from_unit][to_unit](value)
