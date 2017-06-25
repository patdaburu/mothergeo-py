#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.db.postgis.geoalchemy
.. moduleauthor:: Pat Daburu <pat@daburu.net>

How Mother works with  `GeoAlchemy <https://geoalchemy-2.readthedocs.io/en/latest/>`_
"""

from ...geometry import GeometryType
from ..modeling import EntityClass, FeatureClass
from abc import ABCMeta, abstractmethod


class GeoAlchemyEntityClass(EntityClass):
    __metaclass__ = ABCMeta
    __self_properties__ = [
        '_geoalchemy_obj',
        '__geoalchemy_class__'
    ]  # These are the properties that are never deferred to the encapsulated GeoAlchemy object.

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__()
        self._geoalchemy_obj = self.__geoalchemy_class__(**kwargs)

    def __getattr__(self, item):
        if item in self.__self_properties__:
            return self.__dict__[item]
        else:
            return getattr(self._geoalchemy_obj, item)

    def __setattr__(self, key, value):
        if key in self.__self_properties__:
            self.__dict__[key] = value
        else:
            setattr(self._geoalchemy_obj, key, value)

        # To prevent infinite recursion (since we're overriding __getattr__ and __setattr__, let's use the parent
        # class' implementation to get and set our underlying GeoAlchemy classes.

        #geoalchemy_class = super().__getattr__('__geoalchemy_class__')
        #super().__setattr__('_geoalchemy_obj', geoalchemy_class(**kwargs))
        # self.__dict__['_geoalchemy_obj'] = GeoAlchemyEntityClass.__geoalchemy_class__(**kwargs)

    # def __getattr__(self, name):
    #     return getattr(self._geoalchemy_obj, name)
    #     # print(name)
    #     # if hasattr(self._geoalchemy_obj, name):
    #     #     return getattr(self._geoalchemy_obj, name)
    #     # else:
    #     #     return super().__getattr__(self, name)
    #
    # def __setattr__(self, name, value):
    #     setattr(self._geoalchemy_obj, name, value)
    #     # if hasattr(self._geoalchemy_obj, name):
    #     #     setattr(self._geoalchemy_obj, name, value)
    #     # else:
    #     #     super().__setattr__(self, name, value)


class GeoAlchemyFeatureClass(FeatureClass, GeoAlchemyEntityClass):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)




    # @property
    # def _geoalchemy_obj(self):
    #     return self._geoalchemy_obj


