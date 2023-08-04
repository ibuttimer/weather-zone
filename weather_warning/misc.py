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
from enum import Enum

from django.utils.translation import gettext_lazy as _


WARNING_ICON_URL = 'img/warning_icons/icons8-warning-96-{colour}.png'
SMALL_CRAFT_ICON_URL = 'img/warning_icons/icons8-boat-90-{colour}.png'


class Severity(Enum):
    """
    Severity of a warning
    """
    MINOR = (1, 'Minor', 'green')
    MODERATE = (2, 'Moderate', 'yellow')
    SEVERE = (3, 'Severe', 'orange')
    EXTREME = (4, 'Extreme', 'red')

    @classmethod
    def make_translations(cls):
        cls._translations = {
            cls.MINOR: _('Minor'),
            cls.MODERATE: _('Moderate'),
            cls.SEVERE: _('Severe'),
            cls.EXTREME: _('Extreme'),
        }

    @property
    def translation(self):
        return self._translations[self]

    @property
    def number(self):
        return self.value[0]

    @property
    def name(self):
        return self.value[1]

    @property
    def colour(self):
        return self.value[2]

    def awareness_value(self):
        """
        Get the xml value for the Severity enum
        :return:
        """
        return f'{self.value[0]}; {self.value[2]}; {self.value[1]}'

    @classmethod
    def from_awareness(cls, value: str) -> 'Severity':
        """
        Get the Severity enum from an awareness level value
        :param value:
        :return:
        """
        value = value.lower()
        for item in cls:
            if item.awareness_value().lower() == value:
                return item
        raise ValueError(f'No Severity enum for awareness {value}')

    @classmethod
    def from_severity(cls, value: str) -> 'Severity':
        """
        Get the Severity enum from a severity value
        :param value:
        :return:
        """
        value = value.lower()
        for item in cls:
            if item.value[1].lower() == value:
                return item
        raise ValueError(f'No Severity enum for severity {value}')

    def get_icon(self):
        """
        Get the icon for the Severity enum
        :return:
        """
        return WARNING_ICON_URL.format(colour=self.value[2])

    def get_small_crafts_icon(self):
        """
        Get the small crafts icon for the Severity enum
        :return:
        """
        return SMALL_CRAFT_ICON_URL.format(colour=self.value[2])


Severity.make_translations()



class AwarenessType(Enum):
    """
    Awareness type of a warning
    """
    WIND = (1, 'Wind', 'wind')
    SNOW_ICE = (2, 'Snow/Ice', 'snow-ice')
    THUNDERSTORM = (3, 'Thunderstorm', 'thunderstorm')
    FOG = (4, 'Fog', 'fog')
    HIGH_TEMPERATURE = (5, 'High temperature', 'high-temperature')
    LOW_TEMPERATURE = (6, 'Low temperature', 'low-temperature')
    COASTALEVENT = (7, 'Coastal event', 'coastalevent')
    FOREST_FIRE = (8, 'Forest fire', 'forest-fire')
    AVALANCHES = (9, 'Avalanches', 'avalanches')
    RAIN = (10, 'Rain', 'rain')
    FLOODING = (12, 'Flooding', 'flooding')
    RAIN_FLOOD = (13, 'Rain/Flood', 'rain-flood')
    BLIGHT = (21, 'Blight', 'blight')
    ADVISORY = (22, 'Advisory', 'advisory')

    @classmethod
    def make_translations(cls):
        cls._translations = {
            cls.WIND: _('Wind'),
            cls.SNOW_ICE: _('Snow/Ice'),
            cls.THUNDERSTORM: _('Thunderstorm'),
            cls.FOG: _('Fog'),
            cls.HIGH_TEMPERATURE: _('High temperature'),
            cls.LOW_TEMPERATURE: _('Low temperature'),
            cls.COASTALEVENT: _('Coastal event'),
            cls.FOREST_FIRE: _('Forest fire'),
            cls.AVALANCHES: _('Avalanches'),
            cls.RAIN: _('Rain'),
            cls.FLOODING: _('Flooding'),
            cls.RAIN_FLOOD: _('Rain/Flood'),
            cls.BLIGHT: _('Blight'),
            cls.ADVISORY: _('Advisory'),
        }

    @property
    def translation(self):
        return self._translations[self]

    def xml_value(self):
        """
        Get the xml value for the Awareness enum
        :return:
        """
        return f'{self.value[0]}; {self.value[2]}'

    @classmethod
    def from_value(cls, value: str) -> 'AwarenessType':
        """
        Get the Awareness enum from a value
        :param value:
        :return:
        """
        value = value.lower()
        for item in cls:
            if item.xml_value() == value:
                return item
        raise ValueError(f'No AwarenessType enum for value {value}')


AwarenessType.make_translations()
