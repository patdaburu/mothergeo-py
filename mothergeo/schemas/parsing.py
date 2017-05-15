#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.schemas.parsing
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Provide a brief description of the module.
"""

from .modeling import FieldInfo, ModelInfo, Revision, SpatialRelationsCollection
from ..codetools import Dicts
from ..geometry import DEFAULT_SRID
from ..i18n import I18nPack
from functools import wraps
import json


def try_parse(f):
    """
    This is a decorator for "parse" methods that standardizes exceptions as :py:class:`ParseException` instances.

    :param f: the decorated function
    :type f:  ``func``
    :return:  the wrapped function
    :rtype:  ``func``
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except KeyError as k:
            raise ParseException('Key error.') from k
        except FileNotFoundError as fnf:
            raise ParseException('File not found.') from fnf

    return wrapped


class FormatException(Exception):
    """
    Raised when a formatting attempt fails.

    :param message: the exception message
    :type message:  ``str``
    """

    def __init__(self, message):
        super().__init__(message)


class ParseException(Exception):
    """
    Raised when a parsing attempt fails.

    :param message: the exception message
    :type message:  ``str``
    """

    def __init__(self, message):
        super().__init__(message)


class ModelInfoParser(object):
    """
    This is an abstract base class that can be extended to convert between strings and :py:class:`ModelInfo` 
    objects.
    """
    def parse(self, s):
        """
        Override this method in a subclass to parse a string into a :py:class:`Model`.

        :param s: the JSON string you want to parse, or the path to a file containing the JSON
        :type s:  ``str``
        :return: the :py:class:`Model`
        :rtype:  :py:class:`ModelInfo`
        :except: :py:exc:`NotImplementedError`
        """
        raise NotImplementedError('The subclass must override this method.')

    # def format(self, model):
    #     """
    #     Override this method in a subclass to format a :py:class:`ModelInfo` as a JSON string.
    #
    #     :param model: the JSON string you want to parse, or the path to a file containing the JSON
    #     :type model:  :py:class:`ModelInfo`
    #     :return: the JSON string
    #     :rtype:  ``str``
    #     :except: :py:exc:`NotImplementedError`
    #     """
    #     raise NotImplementedError('The subclass must override this method.')


class JsonModelInfoParser(ModelInfoParser):
    """
    This class converts between JSON and :py:class:`ModelInfo` objects.
    """

    def __init__(self):
        super().__init__()

    @try_parse
    def parse(self, s):
        """
        Parse a JSON string into a :py:class:`Model` object.

        :param s: the JSON string you want to parse, or the path to a file containing the JSON
        :type s:  str
        :return: the :py:class:`Model`
        :rtype:  :py:class:`ModelInfo`
        :raises: :py:class:`ParseException` if we can't parse the input.
        """
        parsed = None  # We're going to try a couple of ways to parse the JSON.
        try:  # Let's see if we can just parse the input as JSON.
            json.loads(s)
        except ValueError:
            pass  # Maybe the argument was a file path?
        if parsed is None:  # If we didn't parse the input string successfully...
            with open(s) as json_file:  # ...maybe the caller gave us a file path.
                # So, let's try to parse the contents of the file.
                parsed = json.load(json_file)
        # Let's pull the stuff we want out of the JSON object, like...
        name = Dicts.try_get(parsed, 'name', 'Nameless Model')  # ...the name of the model, and...
        revision = JsonModelInfoParser._json_2_revision(parsed['revision'])  # ...the version (revision), and...
        spatial = JsonModelInfoParser._json_2_spatial_relations(parsed['spatial'])  # ...the spatial relations.
        model = ModelInfo(name=name, revision=revision, spatial_relations=spatial)
        return model

    # def format(self, model):
    #     return None

    @staticmethod
    def _json_2_revision(jsobj):
        """
        Construct a :py:class:`Revision` from the object parsed out of a JSON string.

        :param jsobj: an object parsed from the original JSON string
        :type jsobj:  :py:class:`object`
        :return: the :py:class:`Revision`
        :rtype:  :py:class:`Revision`
        """
        return Revision(title=Dicts.try_get(jsobj, 'title').value,
                        sequence=Dicts.try_get(jsobj, 'sequence').value,
                        author_name=Dicts.try_get(jsobj, 'authorName').value,
                        author_email=Dicts.try_get(jsobj, 'authorEmail').value)

    @staticmethod
    def _json_2_spatial_relations(jsobj):
        # Create a new object with an empty collection of relations.  (We'll fill them in later.)
        common_fields = []
        relations = []
        # Now that we have the information we need, let's create the object.
        return SpatialRelationsCollection(common_fields, relations, Dicts.try_get(jsobj, 'commonSrid', DEFAULT_SRID))

    @staticmethod
    def _json_2_field(jsobj):
        pass

    @staticmethod
    def _json_2_source(jsobj):
        pass

    @staticmethod
    def _json_2_target(jsobj):
        pass

    @staticmethod
    def _json_2_usage(jsobj):
        pass

    @staticmethod
    def _json_2_nena(jsobj):
        pass

    @staticmethod
    def _json_2_i18n(jsobj):
        # Get the default translations.
        defaults = jsobj['default'] if 'default' in jsobj else {}
        # Construct the pack.
        pack = I18nPack(defaults)
        # Get the other (non-default) translation sets.
        for locale in [key for key in filter(lambda key: key != 'default', jsobj.keys())]:
            pack.set_translations(translations=jsobj[locale], locale=locale)
        # That should be all.
        return pack

