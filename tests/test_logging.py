#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mothergeo.logging import loggable_class as loggable


class TestLoggable(unittest.TestCase):
    """
    These test cases test the :py:func:`loggable_class` decorator method.
    """
    def test_loggable_class_without_logger_name(self):
        """
        This test creates a new loggable class without overriding the default logger's name, then creates a new 
        instance and verifies the logger's properties.
        """
        # Define the test class.
        @loggable
        class TestClass(object):
            pass
        # Create an instance of the test class.
        test_obj = TestClass()
        # Verify the test object has a logger.
        self.assertTrue(hasattr(test_obj, 'logger'))
        # Verify the test object logger's name meets the expected pattern.
        self.assertTrue('{module}.{cls}'.format(module=__name__, cls=test_obj.__class__.__name__), test_obj.logger.name)

    def test_loggable_class_with_logger_name(self):
        """
        This test creates a new loggable class, overriding the default logger's name, then creates a new instance and 
        verifies the logger's properties.
        """
        # Define the test class.
        @loggable
        class TestClass(object):
            # Provide the 'logger_name' parameter to override the default logger name.
            logger_name = 'yabba.dabba.doo'
        # Create an instance of the test class.
        test_obj = TestClass()
        # Verify the test object has a logger.
        self.assertTrue(hasattr(test_obj, 'logger'))
        # Verify the test object logger's name meets the value we supplied.
        self.assertTrue('yabba.dabba.doo', test_obj.logger.name)

