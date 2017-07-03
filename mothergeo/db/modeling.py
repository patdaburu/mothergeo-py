#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.db.modeling
.. moduleauthor:: Pat Daburu <pat@daburu.net>

General tools for working with data models in the database.
"""

from ..schemas.modeling import RelationInfo, FeatureTableInfo
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

    def __init__(self):
        self._classes = {}  #: Holds the manufactured classes.

    def _add(self, cls: type):
        self._classes[cls.__name__] = cls

    def get(self, what: RelationInfo or str):
        # The key we'll use to pull the manufactured class from the dictionary is the name applied to the relation
        # information, if that's what the caller gave us.  Otherwise, we assume they're passing in the class name.
        key = what.name if type(what) is RelationInfo else what
        # If we don't have a manufactured class on file with the requested name, but the caller has given us enough
        # information to try to make one...
        if key not in self._classes and type(what) is RelationInfo:
            # ...let's do that now.
            self.make(relation_info=what)
        # Let's return whatever is indexed to the key.
        return self._classes[key]

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


