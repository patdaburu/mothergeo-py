#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.formats.data
.. moduleauthor:: Pat Daburu <pat@daburu.net>

mothergeo data formats.
"""

import json
import numbers
from enum import Enum
from functools import wraps


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


class DataType(Enum):
    """
    These are the supported data types.
    """
    UNKNOWN = 0,
    TEXT = 1,
    UUID = 2,
    INT = 3,
    FLOAT = 4


class DataRequirement(Enum):
    NONE = 0,
    REQUESTED = 1,
    REQUIRED = 2


class Source(object):

    def __init__(self, requirement):
        self._requirement = requirement

    @property
    def requirement(self):
        return self._requirement


class Field(object):
    """
    This class describes a field in a relation (like a table, or a feature class).
    """
    def __init__(self, name, type, width):
        pass


class Revision(object):
    """
    A "revision" contains version information about a model
    """
    def __init__(self, title, sequence, author_name, author_email):
        """
        
        :param title: the revision title
        :type title:  ``str``
        :param sequence: 
        :param author_name: 
        :param author_email: 
        """
        self._title = title
        if sequence is None:
            self._sequence = 0
        elif isinstance(sequence, numbers.Number):
            self._sequence = sequence
        elif isinstance(sequence, str):
            try:
                self._sequence = float(sequence) if '.' in sequence else int(sequence)
            except TypeError as te:
                raise ValueError('sequence must be a number or a convertible string.')
        self._author_name = author_name
        self._author_email = author_email

    @property
    def title(self):
        """
        Get the revision's title.
        
        :return: the title
        :rtype:  ``str``
        """
        return self._title

    @property
    def sequence(self):
        """
        Get the revision's sequence number.

        :return: the sequence number
        :rtype:  ``int`` or ``float``
        """
        return self._sequence

    @property
    def author_name(self):
        """
        Get the name of the person who authored this revision.
        
        :return: the author's name
        :rtype:  ``str``
        """
        return self._author_name

    @property
    def author_email(self):
        """
        Get the email address of the person who authored this revision.
        
        :return: the author's email address
        :rtype:  ``str``
        """
        return self._author_email

    # @staticmethod
    # @try_parse
    # def from_json(s):
    #     json_obj = json.loads(s) if isinstance(s, str) else s
    #     return Revision(title=json_obj['title'],
    #                     sequence=json_obj['sequence'],
    #                     author_name=json_obj['authorName'],
    #                     author_email=json_obj['authorEmail'])


class _Relations(object):
    """
    This is the subclass for collections of information that define the relations (tables) in a :py:class:`Model`.
    """
    def __init__(self, common_fields, relations):
        """
        
        :param common_fields: 
        :type common_fields:  ``list`` of
        :param relations: 
        """
        # If the common_fields variable is a list (as we expect)...
        if isinstance(common_fields, list):
            # ...create an index for the fields that uses the field name as a key.
            self._common_fields = {str(field.name).upper(): field for field in common_fields}
        else:
            raise ValueError('common_fields must be a list.')
        # If the tables variable is a list (as we expect)...
        if isinstance(relations, list):
            # ...create an index for the fields that uses the table's name as a key.
                self._common_fields = {str(field.name).upper(): field for field in common_fields}
        else:
            raise ValueError('relations must be a list.')


class SpatialRelations(_Relations):
    def __init__(self, common_srid, common_fields, relations):
        super().__init__(common_fields=common_fields, relations=relations)
        self._common_srid = common_srid

    @property
    def common_srid(self):
        return self._common_srid


class Model(object):

    def __init__(self, name, revision, spatial_relations):
        self._name = name
        self._revision = revision
        self._spatial_relations = spatial_relations

    @property
    def name(self):
        return self.name

    @property
    def revision(self):
        return self._revision

    @property
    def spatial_relations(self):
        return self._spatial_relations.values()


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


class ModelParser(object):
    """
    This is an abstract base class that can be extended to convert between strings and :py:class:`Model` objects.
    """
    def parse(self, s):
        """
        Override this method in a subclass to parse a string into a :py:class:`Model`.

        :param s: the JSON string you want to parse, or the path to a file containing the JSON
        :type s:  ``str``
        :return: the :py:class:`Model`
        :rtype:  :py:class:`Model`
        :except: :py:exc:`NotImplementedError`
        """
        raise NotImplementedError('The subclass must override this method.')

    # def format(self, model):
    #     """
    #     Override this method in a subclass to format a :py:class:`Model` as a JSON string.
    #
    #     :param model: the JSON string you want to parse, or the path to a file containing the JSON
    #     :type model:  :py:class:`Model`
    #     :return: the JSON string
    #     :rtype:  ``str``
    #     :except: :py:exc:`NotImplementedError`
    #     """
    #     raise NotImplementedError('The subclass must override this method.')


class JsonModelParser(ModelParser):
    """
    This class converts between JSON and :py:class:`Model` objects.
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
        :rtype:  :py:class:`Model`
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
        name = parsed['name']  # ...the name of the model, and...
        revision = JsonModelParser._revision_from_json(parsed['revision'])  # ...the version (revision), and...
        spatial = JsonModelParser._spatial_relations_from_json(parsed['spatial'])  # ...the spatial relations.
        model = Model(name=name, revision=revision, spatial_relations=spatial)
        return model

    # def format(self, model):
    #     return None

    @staticmethod
    def _revision_from_json(json_obj):
        """
        Construct a :py:class:`Revision` from the object parsed out of a JSON string.
        
        :param json_obj: an object parsed from the original JSON string
        :type json_obj:  :py:class:`object`
        :return: the :py:class:`Revision`
        :rtype:  :py:class:`Revision`
        """
        return Revision(title=json_obj['title'],
                        sequence=json_obj['sequence'],
                        author_name=json_obj['authorName'],
                        author_email=json_obj['authorEmail'])

    @staticmethod
    def _spatial_relations_from_json(json_obj):
        return []


