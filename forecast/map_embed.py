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
from typing import Union

from django.conf import settings
from django.utils.http import urlencode

from addresses.models import Address
from forecast import GeoAddress
from utils import html_tag


MAP_EMBED_URL = "https://www.google.com/maps/embed/v1/place?{query}"


def map_embed(address: Union[Address, GeoAddress], width: int = 150, height: int = 150) -> str:
    """
    Create an embedded map for an address

    :param address: Address to create map for
    :return: HTML for embedded map
    """
    query_kwargs = {
        'key': settings.GOOGLE_API_KEY,
    }
    if address.place_id:
        query_kwargs['q'] = f'place_id:{address.place_id}'
    elif address.global_plus_code:
        query_kwargs['q'] = address.global_plus_code
    else:
        query_kwargs['q'] = address.formatted_addr \
            if isinstance(address, Address) else address.formatted_address

    url = MAP_EMBED_URL.format(query=urlencode(query_kwargs))

    return html_tag('iframe', **{
        'width': width,
        'height': height,
        'style': 'border:0',
        'loading': 'lazy',
        'allow': 'fullscreen',
        'src': url,
    })
