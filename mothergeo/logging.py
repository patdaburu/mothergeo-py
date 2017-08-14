#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.logging.rst
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Dear diary...
"""
import logging


def loggable_class(logger_name: str=None):
    """
    This is a decorator you can apply to a class to set it up with a Python ``logger`` property suitable for your
    logging needs.

    :param logger_name: a custom logger name
    :type logger_name:  ``str``
    """
    # We need an inner function that actually adds the logger instance to the class.
    def add_logger(cls):
        # Establish what the name of the logger is going to be.  If the original caller didn't supply one, we'll use
        # a default to construct one.
        _logger_name = logger_name if logger_name is not None else '{module}.{cls}'.format(module=cls.__module__,
                                                                                           cls=cls.__name__)
        # Add a logger property to the class.
        cls.logger = logging.getLogger(_logger_name)
        return cls
    # Return the inner function.
    return add_logger









