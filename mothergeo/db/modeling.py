#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.db.modeling
.. moduleauthor:: Pat Daburu <pat@daburu.net>

General tools for working with data models in the database.
"""

from ..schemas.modeling import  RelationInfo, FeatureTableInfo
from abc import ABCMeta, abstractmethod


class Entity(object):
    """
    Extend this class to model a data entity (like a row in a table).
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        pass


class EntityClassFactory(object):
    """
    Extend this class to create utility classes that can create new entity classes based on the information in a 
    :py:class:`RelationInfo` instance.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def make(self, relation_info: RelationInfo) -> type:
        pass


class Feature(Entity):
    """
    Extend this class to model a feature.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # @property
    # def srid(self):
    #     return self._srid
    #
    # @property
    # def geometry_type(self):
    #     return self._geometry_type


class FeatureTableClassFactory(EntityClassFactory):
    """
    Extend this class to create utility classes that can create new entity classes based on the information in a 
    :py:class:`FeatureTableInfo` instance.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def make(self, relation_info: FeatureTableInfo) -> type:
        pass


