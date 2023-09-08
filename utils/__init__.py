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
from .content_list_mixin import (
    TITLE_CTX, PAGE_HEADING_CTX, LIST_HEADING_CTX, LIST_SUB_HEADING_CTX,
    REPEAT_SEARCH_TERM_CTX, NO_CONTENT_MSG_CTX, NO_CONTENT_HELP_CTX,
    READ_ONLY_CTX, SUBMIT_URL_CTX, SUBMIT_BTN_TEXT_CTX, STATUS_CTX,
    SNIPPETS_CTX, ContentListMixin
)
from .dto import BaseDto
from .enums import (
    ChoiceArg, QueryArg, SortOrder, PerPage6, PerPage8, PerPage50,
    QueryOption, YesNo
)
from .forms import FormMixin
from .html import add_navbar_attr, NavbarAttr, html_tag
from .misc import (
    is_boolean_true, Crud, ensure_list, find_index, dict_drill, AsDictMixin
)
from .models import (
    ModelMixin, ModelFacadeMixin, DESC_LOOKUP, DATE_OLDEST_LOOKUP,
    DATE_NEWEST_LOOKUP
)
from .permissions import (
    permission_name, permission_check, raise_permission_denied
)
from .query_params import QuerySetParams
from .search import (
    ORDER_QUERY, PAGE_QUERY, PER_PAGE_QUERY, REORDER_QUERY, USER_QUERY,
    REORDER_REQ_QUERY_ARGS,
    regex_matchers, MATCH_TERM_GROUP, MATCH_QUERY_GROUP
)
from .singleton import SingletonMixin
from .url_path import (
    append_slash, namespaced_url, app_template_path, url_path, reverse_q,
    query_search_term,
    GET, PATCH, POST, DELETE
)
from .views import resolve_req, redirect_on_success_or_render

__all__ = [
    'TITLE_CTX',
    'PAGE_HEADING_CTX',
    'LIST_HEADING_CTX',
    'LIST_SUB_HEADING_CTX',
    'REPEAT_SEARCH_TERM_CTX',
    'NO_CONTENT_MSG_CTX',
    'NO_CONTENT_HELP_CTX',
    'READ_ONLY_CTX',
    'SUBMIT_URL_CTX',
    'SUBMIT_BTN_TEXT_CTX',
    'STATUS_CTX',
    'SNIPPETS_CTX',
    'ContentListMixin',

    'BaseDto',

    'ChoiceArg',
    'QueryArg',
    'SortOrder',
    'PerPage6',
    'PerPage8',
    'PerPage50',
    'QueryOption',
    'YesNo',

    'FormMixin',

    'add_navbar_attr',
    'NavbarAttr',
    'html_tag',

    'is_boolean_true',
    'Crud',
    'ensure_list',
    'find_index',
    'dict_drill',
    'AsDictMixin',

    'ModelMixin',
    'ModelFacadeMixin',
    'DESC_LOOKUP',
    'DATE_OLDEST_LOOKUP',
    'DATE_NEWEST_LOOKUP',

    'permission_name',
    'permission_check',
    'raise_permission_denied',

    'QuerySetParams',

    'ORDER_QUERY',
    'PAGE_QUERY',
    'PER_PAGE_QUERY',
    'REORDER_QUERY',
    'USER_QUERY',
    'REORDER_REQ_QUERY_ARGS',
    'regex_matchers',
    'MATCH_TERM_GROUP',
    'MATCH_QUERY_GROUP',

    'SingletonMixin',

    'append_slash',
    'namespaced_url',
    'app_template_path',
    'url_path',
    'reverse_q',
    'query_search_term',
    'GET',
    'PATCH',
    'POST',
    'DELETE',

    'resolve_req',
    'redirect_on_success_or_render',
]
