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
from datetime import datetime, timezone
from http import HTTPStatus
import json
from typing import Dict, Tuple
import re
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
import xmltodict
from django.conf import settings

from base import get_request_headers
from forecast import WeatherWarnings, Severity, Category
from forecast.dto import WarningEntry
from utils import dict_drill, ensure_list

from .provider import WarningsProvider


ENCODING_REGEX = re.compile(r'encoding="([^"]+)"')

SUMMARY_ITEMS_DATA_PATH = ['rss', 'channel', 'item']
ITEM_CATEGORY_DATA_PATH = ['alert', 'info', 'category']

WARNINGENTRY_KEY_DATA_PATH = {
    ('alert', 'sent'): WarningEntry.SENT_KEY,
    ('alert', 'msgType'): WarningEntry.MSG_TYPE_KEY,
    ('alert', 'info', 'category'): WarningEntry.CATEGORY_KEY,
    ('alert', 'info', 'event'): WarningEntry.EVENT_KEY,
    ('alert', 'info', 'responseType'): WarningEntry.RESPONSE_KEY,
    ('alert', 'info', 'urgency'): WarningEntry.URGENCY_KEY,
    ('alert', 'info', 'severity'): WarningEntry.SEVERITY_KEY,
    ('alert', 'info', 'certainty'): WarningEntry.CERTAINTY_KEY,
    ('alert', 'info', 'onset'): WarningEntry.ONSET_KEY,
    ('alert', 'info', 'expires'): WarningEntry.EXPIRES_KEY,
    ('alert', 'info', 'headline'): WarningEntry.TITLE_KEY,
    ('alert', 'info', 'description'): WarningEntry.DESCRIPTION_KEY,
    ('alert', 'info', 'instruction'): WarningEntry.INSTRUCTION_KEY,
    ('alert', 'info', 'parameter'): {
        'awareness_level': WarningEntry.AWARENESS_LEVEL_KEY,
        'awareness_type': WarningEntry.AWARENESS_TYPE_KEY,
    },
    ('alert', 'info', 'area', 'areaDesc'): WarningEntry.AREA_DESC_KEY,
    ('alert', 'info', 'area', 'geocode'): WarningEntry.AREAS_KEY,
}

# published date and header modified dates are always in GMT (ignoring DST)
WARNING_PUBLISHED_FMT = "%a, %d %b %Y %H:%M:%S GMT"

CACHED_FILE_MARKER = 'file://'


class MetEireannWarningProvider(WarningsProvider):
    """
    Met Éireann weather warning provider
    """

    def get_warnings(self, **kwargs) -> WeatherWarnings:
        """
        Get weather warnings

        :return: WeatherWarnings
        """

        params = self.url_params(**kwargs)

        # request forecast
        weather_warnings = WeatherWarnings(provider_id=self.name,
                                           provider=self.friendly_name)

        if self.cached_result:
            # cached mode
            reader = read_cached_resp
            url = self.cached_result
        else:
            # live mode
            reader = request_xml
            url = self.data_url

        # load summary
        summary = reader(url, params)
        if summary:
            # load warnings (dict if only 1 else list)
            items = dict_drill(
                summary, *SUMMARY_ITEMS_DATA_PATH, default=[]).value
            for item in ensure_list(items):

                link = warning_link(self, item)     # link to details

                pub_date = gmt_datetime(item)

                warning_info = reader(link, params)
                if warning_info:
                    # take category from summary as in the details 'marine' is
                    # 'met'
                    dict_drill(
                        warning_info, *ITEM_CATEGORY_DATA_PATH, set_new=True,
                        new_value=dict_drill(
                            item, 'category', default='').value)

                    # parse the warning
                    warning = parse_warning(self, warning_info)

                    severity = Severity.from_awareness(warning.awareness_level)
                    warning.icon = severity.get_small_crafts_icon() \
                        if warning.is_small_craft else severity.get_icon()

                    weather_warnings.add_warning(warning)

        return weather_warnings


def parse_warning(provider: WarningsProvider, data: Dict) -> WarningEntry:
    """
    Parse a warning entry from the given data
    :param provider: warning provider
    :param data: dict of warning data
    :return: WarningEntry
    """
    values = {}
    for path, we_k in WARNINGENTRY_KEY_DATA_PATH.items():

        multi_val = isinstance(we_k, dict)     # multiple values in a list flag

        val = dict_drill(data, *path, default='').value
        if we_k in WarningEntry.DATETIME_KEYS:
            # read datetime values
            val = datetime.fromisoformat(val)
        elif multi_val:
            # read multiple values
            val_map = we_k
            for param in val:
                val_name, val_value = read_value_name_val(param)
                we_k = val_map.get(val_name, None)
                if we_k:
                    values[we_k] = val_value
            we_k = None
        elif we_k == WarningEntry.AREAS_KEY:
            # read affected areas
            areas = []
            for area in ensure_list(val):
                val_type, name_val = read_value_name_val(area)
                name_val = provider.regions.get(name_val)
                areas.append(
                    name_val['med_name' if val_type.startswith('FIPS')
                    else 'long_name']
                )
            val = areas
        elif we_k == WarningEntry.CATEGORY_KEY:
            val = Category.from_name(val)
        elif we_k == WarningEntry.SEVERITY_KEY:
            val = Severity.from_name(val)

        if we_k:
            values[we_k] = val

    values.update({
        k: None for k in WarningEntry.KEYS if k not in values
    })
    return WarningEntry(**values)


def read_value_name_val(data: Dict) -> Tuple[str, str]:
    """
    Read the valueName and value from the given data
    :param data:
    :return: valueName, value
    """
    return data['valueName'], data['value']


def request_xml(url: str, params: Dict[str, str]) -> Dict:
    """
    Request xml data from the given url
    :param url:
    :param params:
    :return: response xml as a dict
    """
    xml_resp = '{}'
    try:
        response = requests.get(
            url, params=params, headers=get_request_headers(),
            timeout=settings.REQUEST_TIMEOUT)
        if response.status_code == HTTPStatus.OK:
            xml_resp = response.text
            # HACK - there appears to be a mismatch between the response
            # encoding (ISO-8859-1, 1-byte encoding) and the encoding
            # specified in the xml header (utf8, variable-length character
            # encoding or utf16, 2-byte encoding)
            match = ENCODING_REGEX.search(xml_resp)
            encoding = match.group(1) if match else None
            if (encoding and 'utf' in encoding.lower()
                    and response.encoding == 'ISO-8859-1'):
                # decode the response as utf8
                xml_resp = str(response.content, encoding='utf-8')
            else:
                print(f"WARNING: review xml response; "
                      f"xml encoding ({encoding}), "
                      f"response encoding ({response.encoding})")

    except requests.exceptions.RequestException as e:
        print(e)

    # the 'feedparser' library can't parse the xml returned by
    # Met Éireann as it raises an invalid token exception,
    # so use xmltodict instead

    return xmltodict.parse(xml_resp)


def read_cached_resp(filepath: str, params: Dict[str, str]) -> Dict:
    """
    Read the cached response from the given file path
    :param filepath:
    :param args:
    :return:
    """
    with open(filepath, 'r') as file:
        xml_resp = file.read()
    return xmltodict.parse(xml_resp)


def warning_link(provider: WarningsProvider, item: Dict) -> str:
    """
    Get the warning details link from the given item
    :param provider: warning provider
    :param item: dict of warning data
    :return: http link or file link
    """
    link = dict_drill(item, 'link', default='').value
    if link.startswith(CACHED_FILE_MARKER):
        file = link[len(CACHED_FILE_MARKER):]
        link = str(Path(provider.cached_result).with_name(file))
    return link


def gmt_datetime(item: Dict) -> datetime:
    """
    Extract the published date (GMT) from the given item
    :param item: dict of warning data summary
    :return: GMT datetime
    """
    dt_str = dict_drill(item, 'pubDate', default='').value
    date_time = datetime.min if not dt_str else datetime.strptime(
        dt_str, WARNING_PUBLISHED_FMT).replace(tzinfo=ZoneInfo("GMT"))
    return date_time
