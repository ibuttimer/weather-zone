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

    # severity fields values: Minor/Moderate/Severe/Extreme
    # awareness_level parameter values:
    #   1; green; Minor
    #   2; yellow; Moderate
    #   3; orange; Severe
    #   4; red; Extreme

    @classmethod
    def make_translations(cls):
        cls._translations = {
            cls.MINOR: _('Minor'),
            cls.MODERATE: _('Moderate'),
            cls.SEVERE: _('Severe'),
            cls.EXTREME: _('Extreme'),
        }
        cls._status_translations = {
            cls.MINOR: _('Status Green'),
            cls.MODERATE: _('Status Yellow'),
            cls.SEVERE: _('Status Orange'),
            cls.EXTREME: _('Status Red'),
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

    @property
    def status(self):
        return self._status_translations[self]

    def awareness_value(self):
        """
        Get the xml value for the Severity enum
        :return:
        """
        return f'{self.number}; {self.colour}; {self.name}'

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
    def from_name(cls, value: str) -> 'Severity':
        """
        Get the Severity enum from a name
        :param value:
        :return:
        """
        value = value.lower()
        for item in cls:
            if item.name.lower() == value:
                return item
        raise ValueError(f'No Severity enum for name {value}')

    def get_icon(self):
        """
        Get the icon for the Severity enum
        :return:
        """
        return WARNING_ICON_URL.format(colour=self.colour)

    def get_small_crafts_icon(self):
        """
        Get the small crafts icon for the Severity enum
        :return:
        """
        return SMALL_CRAFT_ICON_URL.format(colour=self.colour)


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
    def number(self):
        return self.value[0]

    @property
    def name(self):
        return self.value[1]

    @property
    def id(self):
        return self.value[2]

    @property
    def translation(self):
        return self._translations[self]

    def xml_value(self):
        """
        Get the xml value for the Awareness enum
        :return:
        """
        return f'{self.number}; {self.id}'

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


class Category(Enum):
    """
    Category of a warning
    """
    MARINE = (1, 'Marine')
    ENVIRONMENTAL = (2, 'Environmental')
    WEATHER = (3, 'Weather')

    @classmethod
    def make_translations(cls):
        cls._translations = {
            cls.MARINE: _('Marine'),
            cls.ENVIRONMENTAL: _('Environmental'),
            cls.WEATHER: _('Weather'),
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

    @classmethod
    def from_name(cls, value: str) -> 'Category':
        """
        Get the Category enum from a name
        :param value:
        :return:
        """
        value = value.lower()
        for item in cls:
            if item.name.lower() == value:
                return item
        raise ValueError(f'No Category enum for name {value}')


Category.make_translations()


class ForecastType(Enum):
    """
    Forecast type
    """
    LOCATION = auto()
    DEFAULT_ADDR = auto()


class AttribRowTypes(Enum):
    """
    Attribute row types
    """
    HEADER = 'hdr'              # header
    WEATHER_ICON = 'img_wi'     # weather icon image
    WIND_DIR_ICON = 'img_wd'    # wind direction icon image
    WIND_SPEED_ICON = 'img_ws'  # wind speed icon image

    @classmethod
    def icon_types(cls):
        return [cls.WEATHER_ICON, cls.WIND_DIR_ICON, cls.WIND_SPEED_ICON]
