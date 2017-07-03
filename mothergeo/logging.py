#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.logging.rst
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Dear diary...
"""
import logging


def loggable_class(cls):
    """
    This is a decorator you can apply to a class to set it up with a Python ``logger`` property suitable for your
    logging.rst needs.
    
    :param cls: the decorated class 
    :type cls:  ``type``
    """
    # Create a variable to hold the reference to the logger.  If the class has specified the 'logger_name' property,
    # we'll use it.  Otherwise, we'll defer until we have a reference to the object.
    _logger = logging.getLogger(cls.logger_name) if hasattr(cls, 'logger_name') else None

    # We need a function that will retrieve the logger.
    def get_logger(obj):
        nonlocal _logger  # Get a reference to the _logger property from the outer scope.
        # If it hasn't been given a value...
        if _logger is None:
            # ...give it the default.
            _logger = logging.getLogger('{module}.{cls}'.format(module=obj.__module__, cls=obj.__class__.__name__))
        return _logger  # This is the answer.
    # Add a logger property to the class.
    cls.logger = property(lambda self: get_logger(self))
    return cls









