#  MIT License
#
#  Copyright (c) 2022-23 Ian Buttimer
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
from typing import Callable, Any, Type, TypeVar, Union

from django.db.models import Q, QuerySet, Model

from .enums import ChoiceArg
from .models import ModelMixin

TypeQuerySetParams = TypeVar("TypeQuerySetParams", bound="QuerySetParams")


class SearchType(Enum):
    """ Enum represent different search result types """
    NONE = auto()
    VALID = auto()
    FREE = auto()       # Free search (no keys specified)
    UNKNOWN = auto()    # Couldn't determine what to search with


class QueryTerm(Enum):
    """ Enum represent different query term types """
    AND = auto()            # AND lookup
    OR = auto()             # OR lookup
    QS_FUNC = auto()        # QuerySet function
    ALL_INC = auto()        # All-inclusive query
    ANNOTATION = auto()     # Annotation


class QuerySetParams:
    """ Class representing query params to be applied to a QuerySet """
    is_distinct: bool
    """ Eliminate duplicate rows flag """
    and_lookups: dict
    """ AND lookups """
    or_lookups: [Q]
    """ OR lookups """
    qs_funcs: [Callable[[QuerySet], QuerySet]]
    """ Functions to apply additional query terms to query set """
    annotations: dict
    """ Annotations """
    params: set
    """ Set of query keys """
    all_inclusive: int
    """
    All-inclusive query count e.g. all statuses require no actual query
    """
    is_none: bool
    """ Empty query set flag """
    search_terms: [str]
    """ List of search terms in set """
    invalid_terms: [str]
    """ List of invalid search terms in set """
    search_type: SearchType
    """ Search result type """

    def __init__(self, is_distinct: bool = True):
        self.is_distinct = is_distinct
        self.and_lookups = {}
        self.or_lookups = []
        self.qs_funcs = []
        self.annotations = {}
        self.params = set()
        self.all_inclusive = 0
        self.is_none = False
        self.search_terms = []
        self.invalid_terms = []
        self.search_type = SearchType.NONE

    def clear(self):
        """ Clear the query set params """
        self.and_lookups.clear()
        self.or_lookups.clear()
        self.qs_funcs.clear()
        self.annotations.clear()
        self.params.clear()
        self.all_inclusive = 0
        self.is_none = False
        self.search_terms = []
        self.invalid_terms = []
        self.search_type = SearchType.NONE

    @property
    def and_count(self):
        """ Count of AND terms """
        return len(self.and_lookups)

    @property
    def or_count(self):
        """ Count of OR terms """
        return len(self.or_lookups)

    @property
    def qs_func_count(self):
        """ Count of functions to apply additional query terms """
        return len(self.qs_funcs)

    @property
    def annotations_count(self):
        """ Count of annotations """
        return len(self.annotations)

    @property
    def is_empty(self):
        """ Check if empty i.e. no query terms """
        return self.and_count + self.or_count + self.qs_func_count \
            + self.annotations_count + self.all_inclusive == 0

    @property
    def is_free_search(self):
        """ Check if free search i.e. value but no query terms """
        return self.search_type == SearchType.FREE

    @property
    def is_unknown_search(self):
        """ Check if unknown search i.e. couldn't determine search criteria """
        return self.search_type == SearchType.UNKNOWN

    def add_and_lookup(self, key: str, lookup: str, value: Any):
        """
        Add an AND lookup
        :param key: query key
        :param lookup: lookup term
        :param value: lookup value
        """
        self.and_lookups[lookup] = value
        self.params.add(key)

    def add_and_lookups(self, key: str, lookups: dict[str, Any]):
        """
        Add an AND lookup
        :param key: query key
        :param lookups: dict with lookup term as key and lookup value
        """
        if isinstance(lookups, dict):
            for lookup, value in lookups.items():
                self.add_and_lookup(key, lookup, value)

    def add_annotation(self, key: str, annotation: str, value: Any):
        """
        Add an annotation
        :param key: query key
        :param annotation: annotation term
        :param value: lookup value
        """
        self.annotations[annotation] = value
        self.params.add(key)

    def add_annotations(self, key: str, annotations: dict[str, Any]):
        """
        Add an AND lookup
        :param key: query key
        :param annotations: dict with annotation term as key and lookup value
        """
        if isinstance(annotations, dict):
            for annotation, value in annotations.items():
                self.add_annotation(key, annotation, value)

    def add(self, query_set_param: TypeQuerySetParams):
        """
        Add lookups from specified QuerySetParams instance
        :param query_set_param: object to add from
        """
        if isinstance(query_set_param, QuerySetParams):
            self.and_lookups.update(query_set_param.and_lookups)
            self.or_lookups.extend(query_set_param.or_lookups)
            self.qs_funcs.extend(query_set_param.qs_funcs)
            self.annotations.update(query_set_param.annotations)
            self.all_inclusive += query_set_param.all_inclusive
            self.params.update(query_set_param.params)
            self.search_terms.extend(query_set_param.search_terms)
            self.invalid_terms.extend(query_set_param.invalid_terms)

    def add_or_lookup(self, key: str, value: Any):
        """
        Add an OR lookup
        :param key: query key
        :param value: lookup value
        """
        if value:
            self.or_lookups.append(value)
            self.params.add(key)

    def add_qs_func(self, key: str, func: Callable[[QuerySet], QuerySet]):
        """
        Add a query term function
        :param key: query key
        :param func: function to apply term
        """
        if func:
            self.qs_funcs.append(func)
            self.params.add(key)

    def add_all_inclusive(self, key: str):
        """
        Add an all-inclusive query term
        :param key: query key
        """
        self.all_inclusive += 1
        self.params.add(key)

    def add_query_term(self, query_type: QueryTerm, key: str,
                       value: Any = None, term: str = None):
        """
        Add a query term
        :param query_type: query type to add, one of QueryTerm
        :param key: query key
        :param value: value, dependent on `query_type`; default None
        :param term: lookup term for QueryTerm.AND or
                    annotation term for QueryTerm.ANNOTATION; default None
        """
        if query_type == QueryTerm.AND:
            self.add_and_lookup(key, term, value)
        elif query_type == QueryTerm.OR:
            self.add_or_lookup(key, value)
        elif query_type == QueryTerm.QS_FUNC:
            self.add_qs_func(key, value)
        elif query_type == QueryTerm.ALL_INC:
            self.add_all_inclusive(key)
        elif query_type == QueryTerm.ANNOTATION:
            self.add_annotation(key, term, value)
        else:
            raise NotImplementedError(f'Unknown query term: {query_type}')

    def add_search_term(self, term: str):
        """
        Add a search term
        :param term: term to add
        """
        self.search_terms.append(term)

    def add_invalid_term(self, term: str):
        """
        Add an invalid search term
        :param term: term to add
        """
        self.invalid_terms.append(term)

    def key_in_set(self, key):
        """
        Check if a query corresponding to the specified `key` has been added
        :param key: query key
        :return: True if added
        """
        return key in self.params

    def apply(self, query_set: QuerySet) -> QuerySet:
        """
        Apply the lookups and term
        :param query_set: query set to apply to
        :return: updated query set
        """
        if self.is_none:
            query_set = query_set.none()
        else:
            query_set = query_set.filter(
                Q(_connector=Q.OR, *self.or_lookups),
                **self.and_lookups)
            for func in self.qs_funcs:
                query_set = func(query_set)
            query_set = query_set.annotate(**self.annotations)
        return query_set.distinct() if self.is_distinct else query_set


def choice_arg_query(
    query_set_params: QuerySetParams, name: str,
    choice_arg: Type[ChoiceArg], all_options: ChoiceArg,
    model: Type[Union[Model, ModelMixin]], search_field: str,
    query: str, and_lookup: str
):
    """
    Process a ChoiceArg query
    :param query_set_params: QuerySetParams instance to update
    :param name: query param
    :param choice_arg: ChoiceArg subclass
    :param all_options: all-inclusive option from `choice_arg`
    :param model: model to search
    :param search_field: field in model to search
    :param query: request query
    :param and_lookup: filed lookup for query
    """
    name = name.lower()
    option = choice_arg.from_arg(name)
    inner_qs = None
    if option is not None:
        # term exactly matches a ChoiceArg arg
        if option == all_options:
            # all options so no need for an actual query term
            query_set_params.add_all_inclusive(query)
        else:
            # get required option
            inner_qs = model.objects.get(**{
                f'{search_field}': option.display
            })
    else:
        # no exact match to ChoiceArg arg, try to match part of search field
        search_param = {
            f'{search_field}__icontains': name
        }
        search_qs = model.objects.filter(**search_param)
        if search_qs.count() == 1:
            # only 1 match, get required option
            inner_qs = model.objects.get(**search_param)
        elif search_qs.count() == 0:
            # TODO no match will result in none result
            pass
        else:
            # multiple matches
            # https://docs.djangoproject.com/en/4.1/topics/db/queries/#complex-lookups-with-q
            query_set_params.add_or_lookup(
                f'{query}-{name}',
                Q(_connector=Q.OR, **{
                    f'{model.id_field()}':
                        stat.id for stat in search_qs.all()
                })
            )

    if inner_qs is not None:
        query_set_params.add_and_lookup(query, and_lookup, inner_qs)
