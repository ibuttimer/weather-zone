"""
Legend classes for locationforecast
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

from weather_zone import settings

from .constants import OLD_ID_PROP, VARIANTS_PROP

BASE_LEGENDS_URL = os.path.join(settings.BASE_DIR,
                                'data/locationforecast/legends.json')
PATCH_LEGENDS_URL = os.path.join(settings.BASE_DIR,
                                 'data/locationforecast/me-legends.json')


class LegendStore:
    """
    Class to store legend data providing multi-key access
    """

    _legends: List[Dict[str, Any]]  # list of legends
    _keys: Dict[str, int]           # key to legend index

    _instance: 'LegendStore' = None # singleton instance

    def __init__(self):
        self._legends = []
        self._keys = {}

    @staticmethod
    def get_instance() -> 'LegendStore':
        """
        Get singleton instance
        :return: LegendStore instance
        """
        if LegendStore._instance is None:
            LegendStore._instance = LegendStore()
        return LegendStore._instance

    def add(self, keys: List[Any], legend: Dict[str, Any]) -> None:
        """
        Add legend data
        :param keys: List of keys to use for access
        :param legend: Legend data
        :return: None
        """
        self._legends.append(legend)
        index = len(self._legends) - 1
        for key in keys:
            if key in self._keys:
                raise KeyError(f"Key '{key}' already exists")
            self._keys[key] = index

    def add_keys(self, key: Any, new_keys: List[Any]) -> None:
        """
        Add additional keys for legend data
        :param key: Key to find legend data
        :param new_keys: List of keys to add to use for access
        :return: None
        """
        if not isinstance(new_keys, list):
            new_keys = [new_keys]
        index = self._keys[key]     # get index of legend data

        for n_key in new_keys:
            if n_key in self._keys:
                raise KeyError(f"Key '{n_key}' already exists")
            self._keys[n_key] = index

    def get(self, key: Any) -> Dict[str, Any]:
        """
        Get legend data
        :param key: Key to use for access
        :return: Legend data
        """
        return self._legends[self._keys[key]]

    def key_exists(self, key: Any) -> bool:
        """
        Check if key exists
        :param key: Key to use for access
        :return: True if key exists, otherwise False
        """
        return key in self._keys


def load_legends() -> LegendStore:
    """
    Load legends
    :return: LegendStore
    """
    # load legends from json file
    with open(BASE_LEGENDS_URL, 'r', encoding='UTF8') as file:
        legends = json.load(file)

    # patch legends from json file
    with open(PATCH_LEGENDS_URL, 'r', encoding='UTF8') as file:
        patch_legends = json.load(file)
        legends.update(patch_legends)

    # convert keys to lower case
    for key in legends.keys():
        if not key.islower():
            legends[key.lower()] = legends.pop(key)

    # "sun": {
    #     "desc_en": "Sun",
    #     "old_id": "1",
    #     "variants": [
    #         "day",
    #         "night",
    #         "polartwilight"
    #     ]
    # },
    # valid keys are ['1', 'sun_day', 'sun_night', 'sun_polartwilight']

    store = LegendStore.get_instance()

    def get_variants(code: str, data: Dict[str, Any]) -> List[str]:
        """
        Get variants for a legend
        :param code: Symbol code
        :param data: Legend data
        :return: List of variants
        """
        keys = []
        variants = data.get(VARIANTS_PROP, None)
        if variants:
            for variant in variants:
                keys.append(f"{code}_{variant}")
        return keys

    for legend, val in legends.items():
        if store.key_exists(val[OLD_ID_PROP]):
            # already have a legend for this id (may have different code but
            # don't care as only use icon and code), so add variants to existing
            # legend
            store.add_keys(val[OLD_ID_PROP], get_variants(legend, val))
        else:
            # add a new legend
            keys = [val[OLD_ID_PROP]]
            keys.extend(get_variants(legend, val))
            store.add(keys, val)

    return store
