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
from .constants import TITLE_CTX, PAGE_HEADING_CTX, PAGE_SUB_HEADING_CTX
from .modal_toast import (
    render_level_info_modal, InfoModalLevel, InfoModalTemplate, IDENTIFIER_CTX,
    level_info_modal_payload
)
from .requests import get_request_headers
from .payloads import (
    redirect_payload, replace_html_payload, replace_inner_html_payload,
    rewrite_payload, entity_delete_result_payload
)


__all__ = [
    'TITLE_CTX',
    'PAGE_HEADING_CTX',
    'PAGE_SUB_HEADING_CTX',

    'render_level_info_modal',
    'InfoModalLevel',
    'InfoModalTemplate',
    'IDENTIFIER_CTX',
    'level_info_modal_payload',

    'get_request_headers',

    'redirect_payload',
    'replace_html_payload',
    'replace_inner_html_payload',
    'rewrite_payload',
    'entity_delete_result_payload',
]
