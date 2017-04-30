#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.codetools
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Helpful utilities from mother.
"""

from enum import Enum
from insensitive_dict import CaseInsensitiveDict


class Enums(object):
    """
    This is a utility class that wants to help you work with :py:class:`Enum` types.
    """
    _names2members = {}  # An index of enumeration member values indexed first by class, then by member name.

    @staticmethod
    def from_name(enum_cls, name):
        """
        Get an enumeration member value from its name.
        
        :param enum_cls: the :py:class:`Enum` ``class``
        :type enum_cls:  ``class``
        :param name: the enumeration member's name
        :type name:  ``str``
        :return: the enumeration member
        :rtype:  :py:class:`Enum`
        """
        # Make sure we're dealing with an Enum type.
        if not issubclass(enum_cls, Enum):
            raise ValueError('enum_class must be of type {typ}'.format(typ=type(Enum)))
        # Now let's get a reference to the index of symbols to their enumeration members.
        symbols2members = None
        # It's possible we haven't see this type before, so we may not have the index on file.
        try:
            symbols2members = Enums._names2members[enum_cls]
        except KeyError:  # This is all right.  It should only happen the first time.
            pass
        # If we haven't already done so...
        if symbols2members is None:
            # ...now's the time to create the index of symbols to the member names.
            symbols2members = CaseInsensitiveDict({
                _name: _member for _name, _member in enum_cls.__members__.items()
            })
            # Now save the collection we just created for next time.
            Enums._names2members[enum_cls] = symbols2members
        # Return the enumeration member indexed to the symbol that was passed in.
        return symbols2members[name]


