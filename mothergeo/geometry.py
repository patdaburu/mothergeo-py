#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.geometry
.. moduleauthor:: Pat Daburu <pat@daburu.net>

General geometry.
"""

from enum import Enum

DEFAULT_SRID = 3857


class GeometryType(Enum):
    """
    These are the supported geometric data types.
    """
    UNKNOWN = 0   #: The geometry type is unknown.
    POINT = 1     #: A point geometry.
    POLYLINE = 2  #: A polyline geometry.
    POLYGON = 3   #: A polygon geometry.
