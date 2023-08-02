"""
Regions classes for locationforecast
"""
import json
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
import os

from typing import List, Dict, Any

from utils import dict_drill
from weather_zone import settings

MARINE_REGIONS_URL = os.path.join(settings.BASE_DIR,
                                  'data/met-eireann/emma.json')
LAND_REGIONS_URL = os.path.join(settings.BASE_DIR,
                                'data/met-eireann/fips.json')

CODES_DATA_PATH = ['codes']


class RegionStore:
    """
    Class to store region data
    """

    _regions: Dict[str, Dict]   # dict of region data

    _instance: 'RegionStore' = None     # singleton instance

    def __init__(self):
        self._regions = {}

    @staticmethod
    def get_instance() -> 'RegionStore':
        """
        Get singleton instance
        :return: RegionStore instance
        """
        if RegionStore._instance is None:
            RegionStore._instance = RegionStore()
        return RegionStore._instance

    def get(self, key: Any) -> Dict[str, Any]:
        """
        Get region data
        :param key: Key to use for access
        :return: region data
        """
        return self._regions[key]

    def key_exists(self, key: Any) -> bool:
        """
        Check if key exists
        :param key: Key to use for access
        :return: True if key exists, otherwise False
        """
        return key in self._regions


def load_regions() -> RegionStore:
    """
    Load regions
    :return: RegionStore
    """
    regions = {}

    for filepath in [MARINE_REGIONS_URL, LAND_REGIONS_URL]:
        with open(filepath, 'r', encoding='UTF8') as file:
            data = json.load(file)
            regions.update(
                dict_drill(data, *CODES_DATA_PATH, default={}).value)

    # convert keys to lower case
    for key in regions:
        if not key.isupper():
            regions[key.upper()] = regions.pop(key)

    store = RegionStore.get_instance()

    store._regions = regions

    return store
