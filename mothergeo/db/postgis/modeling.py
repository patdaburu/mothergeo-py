#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.db.postgis.modeling
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Tools for working with data models in PostGIS.
"""

from ..modeling import ModelTranslator


class PgsqlModelTranslator(ModelTranslator):
    """
    This class converts the information in :py:class:`mothergeo.schemas.modeling.ModelInfo` instances into 
    `PL/pgSQL <https://www.postgresql.org/docs/9.6/static/plpgsql.html>`_ suitable for running against your database.
    """
    def translate(self, model_info, **kwargs):
        """
        Translate a model into a format that your database can understand natively.

        :param model_info: the model
        :type model_info:  :py:class:`mothergeo.schemas.modeling.ModelInfo`
        :return: a PL/pgSQL text representation of the model
        :rtype:  ``str``
        """
        return None
