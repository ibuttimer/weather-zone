"""
Verify the weather icons in the legend.csv file match those in the legends.json file
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
import csv
import json
from dataclasses import dataclass


@dataclass
class CsvEntry:
    """ Class representing a row in the legend.csv file """
    symbol: str
    english: str
    bokmal: str     # Norwegian Bokmål
    nynorsk: str    # Norwegian Nynorsk
    old_id: str
    variants: int


@dataclass
class JsonEntry:
    """ Class representing an entry in the legends.json file """
    symbol: str
    desc_en: str
    desc_nb: str    # Norwegian Bokmål
    desc_nn: str    # Norwegian Nynorsk
    old_id: str
    variants: list[str]


ENTRY_MAP = {
    # csv attr: json attr
    'symbol': 'symbol',
    'english': 'desc_en',
    'bokmal': 'desc_nb',
    'nynorsk': 'desc_nn',
    'old_id': 'old_id',
    'variants': 'variants',
}

csv_entries: list[CsvEntry] = []
json_entries: list[JsonEntry] = []


with open('legend.csv', newline='', encoding='utf8') as csvfile:
    for idx, row in enumerate(csv.reader(csvfile, delimiter=',',)):
        if idx == 0:
            continue
        entry = CsvEntry(*[x.strip() for x in row])
        entry.variants = int(entry.variants)
        csv_entries.append(entry)


with open('legends.json', newline='', encoding='utf8') as jsonfile:
    for key, value in json.load(jsonfile).items():
        args = {
            k: value[k].strip() for k in [
                'desc_en', 'desc_nb', 'desc_nn', 'old_id']
        }
        args.update({
            k: value[k] for k in ['variants']
        })
        args['symbol'] = key.strip()
        json_entries.append(JsonEntry(**args))


for csv_entry in csv_entries:
    found = False
    for json_entry in json_entries:
        found = csv_entry.symbol == json_entry.symbol
        if found:
            for csv_attr, json_attr in ENTRY_MAP.items():
                csv_attr_val = getattr(csv_entry, csv_attr)
                json_attr_val = getattr(json_entry, json_attr)
                if csv_attr == 'variants':
                    csv_attr_val = bool(csv_attr_val)
                    json_attr_val = bool(json_attr_val)
                if csv_attr_val != json_attr_val:
                    print(f"Error: {csv_entry.symbol} {csv_attr} "
                          f"'{csv_attr_val}' differs - '{json_attr_val}'")
            break
    if not found:
        print(f'Not found in json: {csv_entry.symbol}')
