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
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Type

from django.db.models import Model

from utils.misc import ensure_list


@dataclass
class BaseDto:
    """ Base data transfer object """

    add_new: bool = False
    """ Add new placeholder flag"""

    @staticmethod
    def dto_from_model(model: Model, instance: Type['BaseDto'],
                       exclude: List[str] = None) -> Type['BaseDto']:
        """
        Generate a DTO from the specified `model`
        :param model: model class
        :param instance: DTO instance to populate
        :param exclude: names of fields to exclude; default None
        :return: updated instance
        """
        if exclude is None:
            exclude = []
        for key in BaseDto.fields(model):
            if key in exclude:
                continue
            setattr(instance, key, deepcopy(getattr(model, key)))
        return instance

    @staticmethod
    def to_add_new_obj(instance: Type['BaseDto']) -> Type['BaseDto']:
        """
        Generate add new placeholder a DTO from the specified `instance`
        :param instance: DTO instance to update
        :return: updated instance
        """
        instance.add_new = True
        return instance

    @staticmethod
    def fields(model: Model) -> List[str]:
        """
        Get list of model fields
        :param model: model
        :return: list of fields
        """
        return [key for key in list(model.__dict__.keys())
                if not key.startswith('_')]

    @staticmethod
    def model_fields_union(model: Model, fields: List[str]) -> List[str]:
        """
        Get the union of model fields and specified `fields`,
        i.e. elements from model and fields
        :param model: model
        :param fields: fields to add to model fields
        :return: list of fields
        """
        return list(set(BaseDto.fields(model)).union(
            ensure_list(fields)))

    @staticmethod
    def model_fields_intersection(
            model: Model, fields: List[str]) -> List[str]:
        """
        Get the intersection of model fields and specified `fields`,
        i.e. elements common to the model and fields
        :param model: model
        :param fields: fields to determine intersect
        :return: list of fields
        """
        return list(set(BaseDto.fields(model)).intersection(
            ensure_list(fields)))

    @staticmethod
    def model_fields_symmetric_diff(
            model: Model, fields: List[str]) -> List[str]:
        """
        Get the symmetric difference of model fields and specified `fields`,
        i.e. elements in either the model or fields
        :param model: model
        :param fields: fields to determine symmetric difference
        :return: list of fields
        """
        return list(set(BaseDto.fields(model)).symmetric_difference(
            ensure_list(fields)))

    @staticmethod
    def model_fields_difference(
            model: Model, fields: List[str]) -> List[str]:
        """
        Get the difference of model fields and specified `fields`,
        i.e. elements in the model but not in fields
        :param model: model
        :param fields: fields to determine symmetric difference
        :return: list of fields
        """
        return list(set(BaseDto.fields(model)).difference(
            ensure_list(fields)))
