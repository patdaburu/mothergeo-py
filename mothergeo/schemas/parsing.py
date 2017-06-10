#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.schemas.parsing
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Provide a brief description of the module.
"""

from .modeling import (FieldInfo, ModelInfo, NenaSpec, Revision, Source, Target, SpatialRelationsCollection, Usage)
from ..codetools import Dicts
from ..geometry import DEFAULT_SRID
from ..i18n import I18nPack
from functools import wraps
import json


def throws_parse_exception(f):
    """
    This is a decorator for parsing methods that standardizes exceptions as :py:class:`ParseException` instances.

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

    @throws_parse_exception
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
        # Create a new object with an empty collection of relations.
        common_fields = []
        relations = []
        # Now that we have the information we need, let's create the object.
        return SpatialRelationsCollection(
            common_fields, relations, Dicts.try_get(jsobj, 'commonSrid', DEFAULT_SRID).value)

    @staticmethod
    @throws_parse_exception
    def _json_2_field_info(jsobj):
        name = jsobj['name']  # We absolutely require a name.
        unique = Dicts.try_get(jsobj, 'unique', False).value
        data_type = jsobj['type']  # We absolutely require a data type.
        domain = Dicts.try_get(jsobj, 'domain', None).value
        width = Dicts.try_get(jsobj, 'width', None).value
        source = JsonModelInfoParser._json_2_source(jsobj['source'])
        target = JsonModelInfoParser._json_2_target(jsobj['target'])
        usage = JsonModelInfoParser._json_2_usage(Dicts.try_get(jsobj, 'usage', {}).value)
        nena = JsonModelInfoParser._json_2_nena_spec(Dicts.try_get(jsobj, 'nena', {}).value)
        i18n = JsonModelInfoParser._json_2_i18n(jsobj['i18n'])  # We absolutely require I18n information.
        # Now that we have all our information, we can construct a FieldInfo object!
        return FieldInfo(
            name=name, data_type=data_type, source=source, target=target, unique=unique, i18n=i18n, width=width,
            usage=usage, nena=nena, domain=domain)

    @staticmethod
    def _json_2_source(jsobj):
        requirement = Dicts.try_get(jsobj, 'requirement', None).value
        analogs = Dicts.try_get(jsobj, 'analogs', []).value
        source = Source(requirement=requirement, analogs=analogs)
        return source

    @staticmethod
    def _json_2_target(jsobj):
        calculated = Dicts.try_get(jsobj, 'calculated', False).value
        guaranteed = Dicts.try_get(jsobj, 'guaranteed', False).value
        target = Target(calculated=calculated, guaranteed=guaranteed)
        return target

    @staticmethod
    def _json_2_usage(jsobj):
        search = Dicts.try_get(jsobj, 'search', False).value
        display = Dicts.try_get(jsobj, 'display', False).value
        usage = Usage(search=search, display=display)
        return usage

    @staticmethod
    def _json_2_nena_spec(jsobj):
        analog = Dicts.try_get(jsobj, 'analog', None).value
        required = Dicts.try_get(jsobj, 'required', False).value
        nena_spec = NenaSpec(analog=analog, required=required)
        return nena_spec

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

