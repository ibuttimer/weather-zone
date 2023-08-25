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
from dataclasses import dataclass
from enum import Enum

from django.utils.translation import gettext_lazy as _


@dataclass
class BeaufortData:
    """
    Beaufort scale value
    """
    force: int
    description: str
    marine_spec: str
    land_spec: str
    wave_height: float
    wave_height_max: float
    wind_speed_min_knots: float
    wind_speed_max_knots: float
    wind_speed_min_mph: float
    wind_speed_max_mph: float
    wind_speed_min_kmh: float
    wind_speed_max_kmh: float


class Beaufort(Enum):
    """
    Beaufort scale value
    https://www.met.ie/forecasts/marine-inland-lakes/beaufort-scale
    """
    FORCE_0 = BeaufortData(
        0, 'Calm',
        'Smoke rises vertically',
        'Smoke rises vertically',
        0, 0, 1, 1, 1, 1, 1, 1)
    FORCE_1 = BeaufortData(
        1, 'Light air',
        'Ripples',
        'Direction of wind shown by smoke but not by wind vanes',
        0.1, 0.1, 1, 3, 1, 3, 1, 5)
    FORCE_2 = BeaufortData(
        2, 'Light breeze',
        'Small wavelets',
        'Wind felt on face, leaves rustle, ordinary vanes moved by wind',
        0.2, 0.3, 4, 6, 4, 7, 6, 11)
    FORCE_3 = BeaufortData(
        3, 'Gentle breeze',
        'Large wavelets, crests begin to break',
        'Leaves and small twigs in constant motion, wind extends light flag',
        0.6, 1, 7, 10, 8, 12, 12, 19)
    FORCE_4 = BeaufortData(
        4, 'Moderate breeze',
        'Small waves, becoming larger; fairly frequent white horses',
        'Raises dust and loose paper, small branches are moved',
        1, 1.5, 11, 16, 13, 18, 20, 28)
    FORCE_5 = BeaufortData(
        5, 'Fresh breeze',
        'Moderate waves, taking a more pronounced, longer form; many white '
        'horses are formed. Chance of some spray',
        'Small trees in leaf begin to sway, crested wavelets form on inland '
        'waters',
        2, 2.5, 17, 21, 19, 24, 29, 38)
    FORCE_6 = BeaufortData(
        6, 'Strong breeze',
        'Large waves begin to form; the white foam crests are more extensive '
        'everywhere. Some spray',
        'Large branches in motion, whistling heard in electricity wires; '
        'umbrellas used with difficulty',
        3, 4, 22, 27, 25, 31, 39, 49)
    FORCE_7 = BeaufortData(
        7, 'Near gale',
        'Sea heaps up and white foam from breaking waves begins to be blown '
        'in streaks along the direction of the wind',
        'Branches, debris on roads, Loose objects displaced e.g. garden '
        'chairs/bins, Hazardous driving conditions for vulnerable road users, '
        'minor disruption to transport services (air, ferry)',
        4, 5.5, 28, 33, 32, 38, 50, 61)
    FORCE_8 = BeaufortData(
        8, 'Gale',
        'Moderately high waves of greater length; edges of crests begin to '
        'break into spindrift. The foam is blown in well-marked streaks',
        'Small branches, debris on roads, Minor damage to buildings, Damage to '
        'power lines, Power outages, Difficult to walk outdoors, Hazardous '
        'driving conditions, Delays or disruption to some transport services '
        '(air, ferry), Outdoor events cancelled',
        5.5, 7.5, 34, 40, 39, 46, 62, 74)
    FORCE_9 = BeaufortData(
        9, 'Strong gale',
        'High waves. Dense streaks of foam along the direction of the wind. '
        'Crests of waves begin to topple, tumble and roll over',
        'Branches break off, Several fallen trees, Damage to buildings, Damage '
        'to power lines, Widespread power outages, Dangerous conditions, '
        'possible threat to life, Transport services cancelled (air, rail, '
        'ferry, bus), Outdoor events cancelled, Some routes impassable',
        7, 10, 41, 47, 47, 54, 75, 88)
    FORCE_10 = BeaufortData(
        10, 'Storm',
        'Very high waves with long overhanging crests. The resulting foam, '
        'in great patches, is blown in dense white streaks, along the '
        'direction of the wind. The whole surface of the sea takes on a white '
        'appearance. Visibility affected',
        'Seldom experienced inland, Several fallen trees, Damage to buildings, '
        'Damage to power lines, Widespread power outages, Danger to life, '
        'unsafe to be outdoors, Transport services cancelled (air, rail, '
        'ferry, bus), Events cancelled, Several routes impassable',
        9, 12.5, 48, 55, 55, 63, 89, 102)
    FORCE_11 = BeaufortData(
        11, 'Violent storm',
        'Exceptionally high waves (small and medium ships might be, for a '
        'time, lost to view behind the waves). The surface is covered with '
        'long white patches of foam lying along the direction of the wind. '
        'Everywhere, the edges of the wave crests are being blown into the '
        'froth. Visibility affected',
        'Rare inland, Widespread fallen trees, Severe building damage, '
        'Widespread infrastructure damage, Widespread power outages, Danger to '
        'life, unsafe to be outdoors, Isolation of communities, Transport '
        'services cancelled (air, rail, ferry, bus), Only essential services '
        'operating, Many routes impassable',
        11.5, 16, 56, 63, 64, 72, 103, 117)
    FORCE_12 = BeaufortData(
        12, 'Hurricane',
        'The air is filled with foam and spray. Sea completely white with '
        'driving spray.',
        'Very rare inland, Life threatening conditions, Significant and '
        'widespread infrastructure, Widespread and severe building damage, '
        'Widespread fallen trees, Isolation of communities, Disruption to '
        'essential services, Many routes impassable, Transport services '
        'cancelled (air, rail, ferry, bus)',
        14, None, 64, 64, 73, 73, 117, 117)

    @classmethod
    def make_translations(cls):
        cls._translations = {
            cls.FORCE_0: _('Calm'),
            cls.FORCE_1: _('Light air'),
            cls.FORCE_2: _('Light breeze'),
            cls.FORCE_3: _('Gentle breeze'),
            cls.FORCE_4: _('Moderate breeze'),
            cls.FORCE_5: _('Fresh breeze'),
            cls.FORCE_6: _('Strong breeze'),
            cls.FORCE_7: _('Near gale'),
            cls.FORCE_8: _('Gale'),
            cls.FORCE_9: _('Strong gale'),
            cls.FORCE_10: _('Storm'),
            cls.FORCE_11: _('Violent storm'),
            cls.FORCE_12: _('Hurricane'),
        }
        cls._alt_translations_knots = {
            cls.FORCE_0: _('Force 0, less than 1 knot'),
            cls.FORCE_1: _('Force 1, 1-3 knots'),
            cls.FORCE_2: _('Force 2, 4-6 knots'),
            cls.FORCE_3: _('Force 3, 7-10 knots'),
            cls.FORCE_4: _('Force 4, 11-16 knots'),
            cls.FORCE_5: _('Force 5, 17-21 knots'),
            cls.FORCE_6: _('Force 6, 22-27 knots'),
            cls.FORCE_7: _('Force 7, 28-33 knots'),
            cls.FORCE_8: _('Force 8, 34-40 knots'),
            cls.FORCE_9: _('Force 9, 41-47 knots'),
            cls.FORCE_10: _('Force 10, 48-55 knots'),
            cls.FORCE_11: _('Force 11, 56-63 knots'),
            cls.FORCE_12: _('Force 12, 64 knots or more'),
        }
        cls._alt_translations_mph = {
            cls.FORCE_0: _('Force 0, less than 1 mph'),
            cls.FORCE_1: _('Force 1, 1-3 mph'),
            cls.FORCE_2: _('Force 2, 4-7 mph'),
            cls.FORCE_3: _('Force 3, 8-12 mph'),
            cls.FORCE_4: _('Force 4, 13-18 mph'),
            cls.FORCE_5: _('Force 5, 19-24 mph'),
            cls.FORCE_6: _('Force 6, 25-31 mph'),
            cls.FORCE_7: _('Force 7, 32-38 mph'),
            cls.FORCE_8: _('Force 8, 36-46 mph'),
            cls.FORCE_9: _('Force 9, 47-54 mph'),
            cls.FORCE_10: _('Force 10, 55-63 mph'),
            cls.FORCE_11: _('Force 11, 64-72 mph'),
            cls.FORCE_12: _('Force 12, 73 mph or more'),
        }
        cls._alt_translations_kmh = {
            cls.FORCE_0: _('Force 0, less than 1 km/h'),
            cls.FORCE_1: _('Force 1, 1-5 km/h'),
            cls.FORCE_2: _('Force 2, 6-11 km/h'),
            cls.FORCE_3: _('Force 3, 12-19 km/h'),
            cls.FORCE_4: _('Force 4, 20-28 km/h'),
            cls.FORCE_5: _('Force 5, 29-38 km/h'),
            cls.FORCE_6: _('Force 6, 39-49 km/h'),
            cls.FORCE_7: _('Force 7, 50-61 km/h'),
            cls.FORCE_8: _('Force 8, 62-74 km/h'),
            cls.FORCE_9: _('Force 9, 75-88 km/h'),
            cls.FORCE_10: _('Force 10, 89-102 km/h'),
            cls.FORCE_11: _('Force 11, 103-117 km/h'),
            cls.FORCE_12: _('Force 12, 117 km/h or more'),
        }

    @property
    def translation(self):
        return self._translations[self]

    @property
    def alt_translation_knots(self):
        return self._alt_translations_knots[self]

    @property
    def alt_translation_mph(self):
        return self._alt_translations_mph[self]

    @property
    def alt_translations_kmh(self):
        return self._alt_translations_kmh[self]

    @staticmethod
    def from_beaufort(force: int):
        """
        Get the Beaufort enum from a value
        :param force: beaufort force
        :return:
        """
        beaufort = list(filter(lambda x: x.value.force == force, Beaufort))
        return beaufort[0] if beaufort else None


Beaufort.make_translations()
