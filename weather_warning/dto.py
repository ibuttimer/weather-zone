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
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List

from django.utils.translation import gettext as _

from forecast import WeatherWarnings, WarningEntry

from .misc import Severity


@dataclass
class WarningItem:

    ICON_KEY = WarningEntry.ICON_KEY
    ICON_ARIA_KEY = f'{WarningEntry.ICON_KEY}_aria'
    TITLE_KEY = WarningEntry.TITLE_KEY
    DESCRIPTION_KEY = WarningEntry.DESCRIPTION_KEY
    SEVERITY_KEY = WarningEntry.SEVERITY_KEY
    ONSET_KEY = WarningEntry.ONSET_KEY
    EXPIRES_KEY = WarningEntry.EXPIRES_KEY
    SENT_KEY = WarningEntry.SENT_KEY
    INSTRUCTION_KEY = WarningEntry.INSTRUCTION_KEY

    icon: str               # icon to display
    icon_aria: str          # icon aria label
    title: str              # title
    description: str        # description
    onset: str              # expected date/time of onset
    expires: str            # expected date/time of expiry
    sent: str               # time of issue date/time
    instruction: str        # instruction

    _marine: bool = False   # is this a marine warning?
    _small_craft: bool = False  # is this a small craft warning?
    _environmental: bool = False  # is this an environmental warning?
    _weather: bool = False  # is this a weather warning?

    @property
    def is_marine(self) -> bool:
        """
        Is this a marine warning?
        :return: True if marine warning
        """
        return self._marine

    @property
    def is_small_craft(self) -> bool:
        """
        Is this a small craft warning?
        :return: True if small craft warning
        """
        return self._small_craft

    @property
    def is_environmental(self) -> bool:
        """
        Is this an environmental warning?
        :return: True if environmental warning
        """
        return self._environmental

    @property
    def is_weather(self) -> bool:
        """
        Is this a weather warning?
        :return: True if weather warning
        """
        return self._weather

    @staticmethod
    def from_warning_entry(entry: WarningEntry) -> 'WarningItem':
        """
        Create a WarningItem from a WarningEntry
        :param entry:
        :return:
        """
        title = entry.title
        item = WarningItem(
            icon=entry.icon,
            icon_aria=_("%(severity)s. %(desc)s") % {
                "severity": entry.severity.status,
                "desc": entry.description
            },
            title=_("%(severity)s - %(title)s") % {
                "severity": entry.severity.status,
                "title": title
            },
            description=format_description(entry.description),
            onset=format_datetime(entry.onset),
            expires=format_datetime(entry.expires),
            sent=format_datetime(entry.sent),
            instruction=entry.instruction
        )
        item._marine = entry.is_marine
        item._small_craft = entry.is_small_craft
        item._environmental = entry.is_environmental
        item._weather = entry.is_weather
        return item


def format_description(description: str) -> str:
    """
    Format the description
    :param description:
    :return:
    """
    def punc_repl(matchobj):
        return f'{matchobj.group(0)}<br>'

    return re.sub(r'[.:;,]', punc_repl, description)


def format_datetime(dt: datetime) -> str:
    """
    Format a datetime
    :param dt:
    :return:
    """
    return dt.strftime("%H:%M %a %d %b %Y")


class WeatherWarningsDo(WeatherWarnings):
    """
    Weather warnings data object for display purposes
    """
    warnings_do: List[WarningItem]  # list of warnings

    def __init__(self, warnings: WeatherWarnings):
        super().__init__(warnings.provider_id, warnings.provider)
        self.__dict__.update(warnings.__dict__)
        self.warnings_do = list(
            map(WarningItem.from_warning_entry, warnings.warnings))

    @property
    def marine_warning_items(self) -> List[WarningItem]:
        """
        Get the list of marine warnings
        :return: List of marine warnings
        """
        return [w for w in self.warnings_do if w.is_marine]

    @property
    def environmental_warning_items(self) -> List[WarningItem]:
        """
        Get the list of marine warnings
        :return: List of marine warnings
        """
        return [w for w in self.warnings_do if w.is_environmental]

    @property
    def weather_warning_items(self) -> List[WarningItem]:
        """
        Get the list of weather warnings
        :return: List of weather warnings
        """
        return [w for w in self.warnings_do if w.is_weather]
