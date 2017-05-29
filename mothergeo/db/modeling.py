#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.db.modeling
.. moduleauthor:: Pat Daburu <pat@daburu.net>

General tools for working with data models in the database.
"""

# from ..schemas.modeling import  ModelInfo


class DuplicateIdException(Exception):
    """
    Raised when a multiple IDs are defined in a context that should have only one.

    :param message: the exception message
    :type message:  ``str``
    """

    def __init__(self, message):
        super().__init__(message)


class ModelTranslator(object):
    """
    Model translators convert the information stored in :py:class:`mothergeo.schemas.modeling.ModelInfo` instances into
    formats that databases can understand natively.
    """
    def translate(self, model_info, **kwargs):
        """
        Translate a model into a format that your database can understand natively.
        
        :param model_info: the model
        :type model_info:  :py:class:`mothergeo.schemas.modeling.ModelInfo`
        :return: A format that the database can understand.  The subclass will define the return type.
        """
        raise NotImplementedError('The subclass must override this method.')
