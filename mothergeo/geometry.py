#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.geometry
.. moduleauthor:: Pat Daburu <pat@daburu.net>

General geometry.
"""

from enum import Enum

DEFAULT_SRID: int = 3857  #: The default spatial reference ID (SRID)


class GeometryType(Enum):
    """
    These are the supported geometric data types.
    """
    UNKNOWN: int = 0   #: The geometry type is unknown.
    POINT: int = 1     #: A point geometry.
    POLYLINE: int = 2  #: A polyline geometry.
    POLYGON: int = 3   #: A polygon geometry.


class UnsupportedGeometryException(Exception):
    """
    An exception of this type may be thrown if somebody makes an attempt to use a geometry type that isn't supported.

    :param message: the exception message
    :type message:  ``str``
    :param geometry_type: the geometry type
    :type geometry_type:  :py:class:`GeometryType`
    """
    def __init__(self, message: str, geometry_type: GeometryType):
        super().__init__(message)
        self._geometry_type = geometry_type

    @property
    def geometry_type(self) -> GeometryType:
        """
        Get the geometry type.

        :rtype: :py:class:`GeometryType`
        """
        return self._geometry_type
