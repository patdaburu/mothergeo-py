#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.i18n
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Provide a brief description of the module.
"""

from collections import UserDict

class Thing(UserDict):

    def __init__(self, locale, initialdata):
        super().__init__(initialdata)
        self._locale = locale

    @property
    def locale(self):
        return self._locale
