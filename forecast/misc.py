"""
Miscellaneous functions
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
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Tuple

from django.utils.translation import gettext_lazy as _


DateRange = namedtuple('DateRange', ['start', 'end'])


class RangeArg(Enum):
    """
    Range arguments
    """
    TODAY = 'today'
    TOMORROW = 'tomorrow'
    TODAY_PLUS_1 = 'today+1'
    TODAY_PLUS_2 = 'today+2'
    TODAY_PLUS_3 = 'today+3'
    TODAY_PLUS_4 = 'today+4'
    TOMORROW_PLUS_1 = 'tomorrow+1'
    TOMORROW_PLUS_2 = 'tomorrow+2'
    TOMORROW_PLUS_3 = 'tomorrow+3'
    ALL = 'all'

    def as_dates(self) -> DateRange:
        """
        Convert to date range
        :return: date range
        """
        if self == RangeArg.ALL:
            start, end = (None, None)
        else:
            start = datetime.now(tz=timezone.utc)
            if 'tomorrow' in self.value:
                start += timedelta(days=1)
                start = start.replace(hour=0, minute=0, second=0, microsecond=0)

            # calc end
            end = start + timedelta(days=1)
            end = end.replace(hour=0, minute=0, second=0, microsecond=0)
            if '+' in self.value:
                end += timedelta(days=int(self.value.split('+')[1]))

        return DateRange(start, end)

    @classmethod
    def from_str(cls, arg: str) -> 'RangeArg':
        """
        Convert string to enum
        :param arg: string to convert
        :return: enum
        """
        return cls[arg.upper().replace('+', '_PLUS_')]


def get_range_choices() -> Tuple[Tuple[str, str]]:
    """
    Get range choices
    :return: range choices
    """
    return tuple([
        (RangeArg.TODAY.value, _('Today')),
        (RangeArg.TOMORROW.value, _('Tomorrow')),
        (RangeArg.TODAY_PLUS_1.value, _('Next 2 days')),
        (RangeArg.TODAY_PLUS_2.value, _('Next 3 days')),
        (RangeArg.TODAY_PLUS_3.value, _('Next 4 days')),
        (RangeArg.TODAY_PLUS_4.value, _('Next 5 days')),
        (RangeArg.TOMORROW_PLUS_1.value, _('Tomorrow 2 days')),
        (RangeArg.TOMORROW_PLUS_2.value, _('Tomorrow 3 days')),
        (RangeArg.TOMORROW_PLUS_3.value, _('Tomorrow 4 days')),
        (RangeArg.ALL.value, _('All available')),
    ])
