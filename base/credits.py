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

from django.utils.translation import gettext_lazy as _

from utils import html_tag

IconInfo = namedtuple(
    'IconInfo',
    ['name', 'provider', 'conjunction', 'icon_url', 'provider_url'],
    defaults=['', '', '', '', '']
)

ICONS_BY = _('icons by')
ICON_BY = _('icon by')
ICONS_DERIVED_FROM = _('icons derived from')
ICON_CREATED_BY = _('icon created by')

ICONS = [
    IconInfo(
        name='Weather forecast logo', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/kLj4x6XyooyO/weather-forecast',
        provider_url='https://icons8.com'),
    IconInfo(
        name='Weather forecast',
        provider='The Norwegian Broadcasting Corporation',
        conjunction=ICONS_BY,
        icon_url='https://nrkno.github.io/yr-weather-symbols/',
        provider_url='https://www.nrk.no/'),
    IconInfo(
        name='Warning', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/KarJz0n4bZSj/general-warning-sign',
        provider_url='https://icons8.com'),
    IconInfo(
        name='Boat', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/66056/sail-boat',
        provider_url='https://icons8.com'),
    IconInfo(
        name='A', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/38670/a',
        provider_url='https://icons8.com'),
    IconInfo(
        name='Breeze', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/DSEt3IYZwWNb/breeze',
        provider_url='https://icons8.com'),
    IconInfo(
        name='Breeze', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/i90FKzAM6LYA/breeze',
        provider_url='https://icons8.com'),
    IconInfo(
        name='Wind', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/74197/wind',
        provider_url='https://icons8.com'),
    IconInfo(
        name='Storm', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/EKkPq7Olo1Hp/storm',
        provider_url='https://icons8.com'),
    IconInfo(
        name='Tornado', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/9309/tornado',
        provider_url='https://icons8.com'),
    IconInfo(
        name='Nothing Found', provider='Icons8', conjunction=ICON_BY,
        icon_url='https://icons8.com/icon/83786/nothing-found',
        provider_url='https://icons8.com'),
    IconInfo(
        name='Wind direction',
        provider='South icons created by Freepik - Flaticon',
        conjunction=ICONS_DERIVED_FROM,
        icon_url='https://www.flaticon.com/free-icons/south',
        provider_url='https://www.flaticon.com'),
    IconInfo(
        name='404 error',
        provider='Freepik - Flaticon',
        conjunction=ICON_CREATED_BY,
        icon_url='https://www.flaticon.com/free-icons/404-error',
        provider_url='https://www.flaticon.com'),
    IconInfo(
        name='Explosion',
        provider='Freepik - Flaticon',
        conjunction=ICON_CREATED_BY,
        icon_url='https://www.flaticon.com/free-icons/explosion',
        provider_url='https://www.flaticon.com'),
    IconInfo(
        name='Stop sign',
        provider='Freepik - Flaticon',
        conjunction=ICON_CREATED_BY,
        icon_url='https://www.flaticon.com/free-icons/stop-sign',
        provider_url='https://www.flaticon.com'),
    IconInfo(
        name='Confusion',
        provider='Freepik - Flaticon',
        conjunction=ICON_CREATED_BY,
        icon_url='https://www.flaticon.com/free-icons/confusion',
        provider_url='https://www.flaticon.com'),
]


def icon_entry(icon: IconInfo) -> str:
    icon_aria = _(
        "open icon on %(provider)s in another tab"
    ) % {'provider': icon.provider}
    icon_link = html_tag('a', icon.name, **{
        'href': icon.icon_url,
        'aria-label': icon_aria,
        'target': '_blank',
        'rel': 'noopener'
    })
    provider_aria = _(
        "open %(provider)s in another tab") % {'provider': icon.provider}
    provider_link = html_tag('a', icon.provider, **{
        'href': icon.provider_url,
        'aria-label': provider_aria,
        'target': '_blank',
        'rel': 'noopener'
    })
    return f'{icon_link} {icon.conjunction} {provider_link}'


ICON_CREDITS = list(map(icon_entry, ICONS))
