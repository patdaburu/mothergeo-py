#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.formats.data
.. moduleauthor:: Pat Daburu <pat@daburu.net>

mothergeo data formats.
"""

from insensitive_dict import CaseInsensitiveDict
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
    UNKNOWN = 0  #: The data type is unknown.
    TEXT = 1     #: This is character data.
    UUID = 2     #: This is a universally unique identifier.
    INT = 3      #: This is an integer.
    FLOAT = 4    #: This is a floating-point number.


class Requirement(Enum):
    """
    How important is it that data be provided?  For example, a data field that is ``REQUESTED`` is a field for which we
    may ask, but a field that is ``REQUIRED`` *must* have data in it it.
    """
    NONE = 0       #: There is no requirement for this data to be present.
    REQUESTED = 1  #: We would like the data to be present.
    REQUIRED = 2   #: The data *must* be present.


class Source(object):
    """
    This object provides information about our expectations regarding the source from which data comes.
    """
    def __init__(self, requirement):
        self._requirement = requirement

    @property
    def requirement(self):
        """
        Is this data required? or requested? or neither?
        
        :return:  the data requirement 
        :rtype:   :py:class:`Requirement`
        """
        return self._requirement


class Field(object):
    """
    This class describes a field in a relation (like a table, or a feature class).
    """
    def __init__(self, name, data_type, width=None):
        """
        
        :param name: the field's name
        :type name:  ``str``
        :param data_type: the field's data type
        :type data_type:  :py:class:`DataType`
        :param width: the field's width
        :type width:  ``int``
        """
        self._name = name
        self._data_type = data_type
        self._width = width

    @property
    def name(self):
        """
        This is the field's name.
        
        :return: the field's name
        :rtype:  ``str``
        """
        return self._name

    @property
    def data_type(self):
        """
        This is the field's data type.
        
        :return: the field's data type
        :rtype:  :py:class:`DataType`
        """
        return self._data_type

    @property
    def width(self):
        """
        This is the field's width.
        
        :return: the field's width
        :rtype:  ``str``
        """
        return self._width


class Revision(object):
    """
    A "revision" contains version information about when a model was defined.
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
                raise TypeError('sequence must be a number or a convertible string.') from te
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


class _Relation(object):
    pass


class _Relations(object):
    """
    This is the subclass for collections of information that define the relations (tables) in a :py:class:`Model`.
    """
    def __init__(self, common_fields, relations):
        """
        
        :param common_fields: the common fields shared among relations in this collection
        :type common_fields:  ``list`` of :py:class:`Field`
        :param relations: the relations in this collection
        :type relations:  :py:class:_Relation
        """
        # If we didn't get any common fields...
        if common_fields is None:
            self._common_fields = {}  # ...our internal index is empty.
        elif isinstance(common_fields, list):  # If we got the type we expect...
            # ...create an index for the fields that uses the field name as a key.
            self._common_fields = CaseInsensitiveDict({str(field.name): field for field in common_fields})
        else:
            raise ValueError('common_fields must be a list.')
        # If we didn't get any relations...
        if relations is None:
            self._relations = {}  # ...our internal index is empty.
        elif isinstance(relations, list):  # If we got the type we expect...
            # ...create an index for the fields that uses the table's name as a key.
                self._relations = CaseInsensitiveDict({str(field.name): field for field in relations})
        else:
            raise ValueError('relations must be a list.')

    def __iter__(self):
        # Return the values in the _relations index.
        return iter(self._relations.values())

    def get_common_field(self, name):
        """
        Get a common field from the collection.
        
        :param name: the field name
        :type name:  ``str``
        :return: the field
        :rtype:  :py:class:`Field`
        """
        if name is None:
            raise TypeError("name cannot be None.")
        elif name not in self._common_fields:
            raise KeyError("Common field '{name)' is not defined.".format(name=name))
        else:
            return self._relations[name]

    def get_relation(self, name):
        """
        Get a relation from the collection.

        :param name: the relation's name
        :type name:  ``str``
        :return: the relation
        :rtype:  :py:class:`_Relation`
        """
        if name is None:
            raise TypeError("name cannot be None.")
        elif name not in self._common_fields:
            raise KeyError("Relation '{name)' is not defined.".format(name=name))
        else:
            return self._relations[name]



class SpatialRelations(_Relations):
    def __init__(self, common_srid, common_fields, relations):
        super().__init__(common_fields=common_fields, relations=relations)
        self._common_srid = common_srid

    @property
    def common_srid(self):
        return self._common_srid


class Model(object):
    """
    Instances of this class describe a data model.
    """
    def __init__(self, name, revision, spatial_relations):
        self._name = name
        self._revision = revision
        self._spatial_relations = spatial_relations

    @property
    def name(self):
        """
        Get the model's name.
        
        :return: the model's name
        :rtype:  ``str``
        """
        return self._name

    @property
    def revision(self):
        """
        Get the model's revision information.
        
        :return: the model's revision information
        :rtype:  :py:class:`Revision`
        """
        return self._revision

    @property
    def spatial_relations(self):
        """
        Get the model's spatial relation information.
        
        :return: the model's spatial relation information
        :rtype:  :py:class:`SpatialRelations`
        """
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


