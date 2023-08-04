"""
Data transfer objects for forecast module
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
from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Tuple, Set, Callable, Optional

from weather_warning.misc import Severity


@dataclass
class WarningEntry:
    """
    Warning entry
    """
    SENT_KEY = 'sent'
    MSG_TYPE_KEY = 'msg_type'
    CATEGORY_KEY = 'category'
    EVENT_KEY = 'event'
    RESPONSE_KEY = 'response'
    URGENCY_KEY = 'urgency'
    SEVERITY_KEY = 'severity'
    CERTAINTY_KEY = 'certainty'
    ONSET_KEY = 'onset'
    EXPIRES_KEY = 'expires'
    TITLE_KEY = 'title'
    DESCRIPTION_KEY = 'description'
    INSTRUCTION_KEY = 'instruction'
    AWARENESS_LEVEL_KEY = 'awareness_level'
    AWARENESS_TYPE_KEY = 'awareness_type'
    AREAS_KEY = 'areas'
    ICON_KEY = 'icon'

    sent: datetime          # time of issue date/time
    msg_type: str           # message type: Alert/Update/Cancel
    category: str           # category: Environmental/Marine/Weather
    event: str              # event
    # response type: Monitor [Shelter|Evacuate|Prepare|Avoid|AllClear|None]
    response: str
    urgency: str            # urgency: Future [Past, Immediate, Expected]
    severity: str           # severity: Minor/Moderate/Severe/Extreme
    certainty: str          # Likely [Possible/Observed/Unlikely]
    onset: datetime         # expected date/time of onset
    expires: datetime       # expected date/time of expiry
    title: str              # title
    description: str        # description
    instruction: str        # instruction
    awareness_level: str    # awareness level; e.g. 2; yellow; Moderate
    awareness_type: str     # awareness level; e.g. 1; Wind
    areas: List[str]        # list of areas affected

    icon: str               # icon to display

    @classmethod
    def set_key_lists(cls):
        cls.KEYS = [
            v for k, v in cls.__dict__.items()
            if k not in object.__dict__ and not k.startswith('_')
            and k.endswith('_KEY') and not callable(v)
        ]
        cls.DATETIME_KEYS = [
            cls.SENT_KEY, cls.ONSET_KEY, cls.EXPIRES_KEY]

    def is_category(self, category: str) -> bool:
        """
        Is this a warning of category?
        :return: True if is category warning
        """
        return self.category.lower() == category.lower()

    def is_marine(self) -> bool:
        """
        Is this a marine warning?
        :return: True if marine warning
        """
        return self.is_category('marine')

    def is_small_craft(self) -> bool:
        """
        Is this a small craft warning?
        :return: True if small craft warning
        """
        return 'small craft advisory' in self.event.lower()

    def is_environmental(self) -> bool:
        """
        Is this an environmental warning?
        :return: True if environmental warning
        """
        return self.is_category('environmental')

    def is_weather(self) -> bool:
        """
        Is this a weather warning?
        :return: True if weather warning
        """
        return self.is_category('weather')


WarningEntry.set_key_lists()


class WeatherWarnings:
    """
    Weather warnings
    """
    created: datetime  # date/time warnings was created
    provider: str  # name of forecast provider
    warnings: List[WarningEntry]  # list of warnings
    cached: bool  # is this a cached forecast?

    def __init__(self, provider: str = ''):
        self.created = datetime.now()
        self.provider = provider
        self.warnings = []
        self.cached = False

    def add_warning(self, warning: WarningEntry):
        """
        Add a warning
        :param warning: Warning to add
        """
        self.warnings.append(warning)

    @property
    def marine_count(self) -> int:
        """
        Get the number of marine warnings
        :return: Number of marine warnings
        """
        return len([w for w in self.warnings if w.is_marine()])

    @property
    def environmental_count(self):
        """
        Get the number of marine warnings
        :return: Number of marine warnings
        """
        return len([w for w in self.warnings if w.is_environmental()])

    @property
    def weather_count(self):
        """
        Get the number of weather warnings
        :return: Number of weather warnings
        """
        return len([w for w in self.warnings if w.is_weather()])

    def _highest_severity_level(self, filter_fxn: Callable) -> Optional[Severity]:
        """
        Get highest severity level of warnings
        :param filter_fxn: Filter function
        :return: Highest severity
        """
        return max(
            map(lambda w: Severity.from_severity(w.severity),
                filter(filter_fxn, self.warnings)
            ),
            key=lambda s: s.number
        )

    @property
    def highest_marine_level(self) -> Optional[Severity]:
        """ Highest severity level of marine warning """
        return self._highest_severity_level(lambda w: w.is_marine())

    @property
    def highest_weather_level(self) -> Optional[Severity]:
        """ Highest severity level of weather warning """
        return self._highest_severity_level(lambda w: w.is_weather())

    @property
    def highest_environmental_level(self) -> Optional[Severity]:
        """ Highest severity level of environmental warning """
        return self._highest_severity_level(lambda w: w.is_environmental())

    @property
    def highest_marine_level_icon(self) -> Optional[str]:
        """ Icon for highest severity level of marine warning """
        severity = self.highest_marine_level
        return severity.get_icon() if severity else None

    @property
    def highest_weather_level_icon(self) -> Optional[str]:
        """ Icon for highest severity level of weather warning """
        severity = self.highest_weather_level
        return severity.get_icon() if severity else None

    @property
    def highest_environmental_level_icon(self) -> Optional[str]:
        """ Icon for highest severity level of environmental warning """
        severity = self.highest_environmental_level
        return severity.get_icon() if severity else None
