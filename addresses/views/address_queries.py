#  MIT License
#
#  Copyright (c) 2023 Ian Buttimer
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#
from enum import Enum, auto
from typing import Any

from django.db.models import QuerySet

from user.models import User

from ..enums import AddressType
from ..models import Address
from utils import (
    regex_matchers, QuerySetParams,
    MATCH_TERM_GROUP, MATCH_QUERY_GROUP,
    USER_QUERY
)

# context-related
DEFAULT_ADDRESS_QUERY: str = 'dflt-addr'    # display default address modal

NON_DATE_QUERIES = [
    USER_QUERY
]
REGEX_MATCHERS = regex_matchers(NON_DATE_QUERIES)

FIELD_LOOKUPS = {
    # query param: filter lookup
    USER_QUERY: f'{Address.USER_FIELD}__{User.USERNAME_FIELD}',
}
# priority order list of query terms
FILTERS_ORDER = [
    # search is a shortcut filter, if search is specified nothing
    # else is checked after therefore must be first
]
ALWAYS_FILTERS = [
    # always applied items
]
FILTERS_ORDER.extend(
    [q for q in FIELD_LOOKUPS if q not in FILTERS_ORDER]
)
# complex queries which require more than a simple lookup or context-related
NON_LOOKUP_ARGS = [
    DEFAULT_ADDRESS_QUERY,
]

SEARCH_REGEX = [
    # regex,            query param, regex match group, key & regex match grp
    (REGEX_MATCHERS[q], q,           MATCH_TERM_GROUP,        MATCH_QUERY_GROUP)
    for q in NON_DATE_QUERIES
]


class QueryParam(Enum):
    """ Enum representing options for QuerySet creation """
    FILTER = auto()
    EXCLUDE = auto()


def get_lookup(
    query: str, value: Any, user: User,
    query_set_params: QuerySetParams = None
) -> QuerySetParams:
    """
    Get the query lookup for the specified value
    :param query: request query argument
    :param value: argument value
    :param user: current user
    :param query_set_params: query set params
    :return: query set params
    """
    if query_set_params is None:
        query_set_params = QuerySetParams()
    if value is None:
        return query_set_params

    # if query == SEARCH_QUERY:
    #     query_set_params = get_search_term(
    #         value, user, query_set_params=query_set_params)
    if query not in NON_LOOKUP_ARGS and value:
        query_set_params.add_and_lookup(query, FIELD_LOOKUPS[query], value)
    # else no value or complex query term handled elsewhere

    return query_set_params


# def get_search_term(
#     value: str, user: User, query_set_params: QuerySetParams = None
# ) -> QuerySetParams:
#     """
#     Generate search terms for specified input value
#     :param value: search value
#     :param user: current user
#     :param query_set_params: query set params
#     :return: query set params
#     """
#     if query_set_params is None:
#         query_set_params = QuerySetParams()
#     if value is None:
#         return query_set_params
#
#     for regex, query, group, key_val_group in SEARCH_REGEX:
#         match = regex.match(value)
#         if match:
#             success = True
#             if query not in NON_LOOKUP_ARGS:
#                 query_set_params.add_and_lookup(
#                     query, FIELD_LOOKUPS[query], match.group(group))
#             else:
#                 # complex query term handled elsewhere
#                 success = False
#
#             save_term_func = query_set_params.add_search_term if success \
#                 else query_set_params.add_invalid_term
#             save_term_func(match.group(key_val_group))
#
#     return query_set_params


def addresses_query(user: User = None,
                    address_type: AddressType = AddressType.ALL,
                    action: QueryParam = QueryParam.FILTER) -> QuerySet:
    """
    Get addresses
    :param user: user to get addresses for; default None i.e. all addresses
    :param address_type: address type; default AddressType.ALL
    :param action: query action; default QueryParam.FILTER
    :return: addresses
    """
    params = {}
    if user:
        params[f'{Address.USER_FIELD}'] = user
    if address_type in [AddressType.DEFAULT, AddressType.NON_DEFAULT]:
        params[f'{Address.IS_DEFAULT_FIELD}'] = \
            address_type == AddressType.DEFAULT

    if action == QueryParam.FILTER:
        query_set = Address.objects.filter(**params)
    elif action == QueryParam.EXCLUDE:
        query_set = Address.objects.exclude(**params)
    else:
        raise NotImplementedError(f'Unknown param {action}')
    return query_set
