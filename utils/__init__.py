"""
Module for utility functions
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
from .forms import FormMixin
from .html import add_navbar_attr, NavbarAttr, html_tag
from .misc import (
    is_boolean_true, Crud, ensure_list, find_index, dict_drill
)
from .url_path import (
    append_slash, namespaced_url, app_template_path, url_path, reverse_q,
    GET, PATCH, POST, DELETE
)
from .views import resolve_req, redirect_on_success_or_render

__all__ = [
    'FormMixin',

    'add_navbar_attr',
    'NavbarAttr',
    'html_tag',

    'is_boolean_true',
    'Crud',
    'ensure_list',
    'find_index',
    'dict_drill',

    'append_slash',
    'namespaced_url',
    'app_template_path',
    'url_path',
    'reverse_q',
    'GET',
    'PATCH',
    'POST',
    'DELETE',

    'resolve_req',
    'redirect_on_success_or_render',
]
