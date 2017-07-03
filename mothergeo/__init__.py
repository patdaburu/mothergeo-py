#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo
.. moduleauthor:: Pat Daburu <pat@daburu.net>

GIS handling that cares.
"""

import logging

__version__ = '0.0.1'
__release__ = '0.0.1'

# Set default logging.rst handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())


class Test(object):
    """
    A test class.
    """

    def do_something(self):
        """
        A test method.
        
        :return: Here's what I return.
        :rtype: ``str``
        """
        return 'x'

