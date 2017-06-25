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
