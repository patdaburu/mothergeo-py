#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.schemas.modeling
.. moduleauthor:: Pat Daburu <pat@daburu.net>

The shape data takes.
"""

from ..codetools import Enums
from ..i18n import I18nPack
from mothergeo.geometry import DEFAULT_SRID, GeometryType
from insensitive_dict import CaseInsensitiveDict
from typing import List, Iterator

import numbers
from enum import Enum


class DataType(Enum):
    """
    These are the supported data types.
    """
    UNKNOWN = 'UNKNOWN'    #: The data type is unknown.
    TEXT = 'TEXT'          #: This is character data.
    UUID = 'UUID'          #: This is a universally unique identifier.
    INT = 'INT'            #: This is an integer.
    FLOAT = 'FLOAT'        #: This is a floating-point number.
    DATETIME = 'DATETIME'  #: This is a moment in time.


class Requirement(Enum):
    """
    How important is it that data be provided?  For example, a data field that is ``REQUESTED`` is a field for which we
    may ask, but a field that is ``REQUIRED`` *must* have data in it it.
    """
    NONE = 'NONE'            #: There is no requirement for this data to be present.
    REQUESTED = 'REQUESTED'  #: We would like the data to be present.
    REQUIRED = 'REQUIRED'    #: The data *must* be present.


class Source(object):
    """
    Source objects provide information about our expectations regarding the source from which data comes.
    """

    def __init__(self, requirement, analogs=None):
        """
        :param requirement: the requirement placed upon the source
        :type requirement:  :py:class:`Requirement` or ``str``
        :seealso: :py:func:`Source.requirement`
        :param analogs:  a list of analogous field name patterns
        :type analogs:  list(str) or None
        :seealso: :py:func:`Source.analogs`
        """
        self._requirement = Enums.from_name(Requirement, requirement) if requirement is not None else None
        self._analogs = analogs if type(analogs) is list else [analogs] if analogs is not None else []

    @property
    def requirement(self) -> Requirement:
        """
        Is this data required? or requested? or neither?
        
        :return:  the data requirement 
        :rtype:   :py:class:`Requirement`
        """
        return self._requirement

    @property
    def analogs(self) -> List[str]:
        """
        This is a list of common analogous field name patterns.
        
        :return: the analogous field name patterns
        :rtype:  list(str)
        """
        return self._analogs


class Target(object):
    """
    Source objects describe the contract presented to the consumer of the target data.
    """
    def __init__(self, calculated: bool=False, guaranteed: bool=False):
        """
        
        :param calculated: May this data be calculated? 
        :type calculated:  ``bool``
        :seealso: :py:func:`Target.guaranteed`
        :param guaranteed: Is this data guaranteed to have a non-empty value?
        :type calculated:  ``bool``
        :seealso: :py:func:`Target.guaranteed`
        """
        self._calculated = calculated
        self._guaranteed = guaranteed

    @property
    def calculated(self) -> bool:
        """
        May this data be calculated?
        
        :rtype:  ``bool`` 
        """
        return self._calculated

    @property
    def guaranteed(self) -> bool:
        """
        Is this data guaranteed to have a non-empty value?
        
        :rtype:  ``bool``
        """
        return self._guaranteed


class Usage(object):
    """
    Usage objects provide information about how data should be used.
    """
    def __init__(self, search: bool=False, display: bool=False):
        """ 
        :param search: is this data intended to be used in searches?
        :type search:  ``bool``
        :seealso: :py:func:`Usage.search`
        :param display: is this data intended to be displayed to humans?
        :type display:  ``bool``
        :seealso: :py:func:`Usage.display`
        """
        self._search = search
        self._display = display

    @property
    def search(self) -> bool:
        """
        Is this data intended to be used in searches?
        
        :rtype:  ``bool`` 
        """
        return self._search

    @property
    def display(self) -> bool:
        """
        Is this data intended to be displayed to humans?
        
        :rtype:  ``bool``
        """
        return self._display


class NenaSpec(object):
    """
    NENA information objects describe how data relates to the `NENA standard <http://bit.ly/2qEGGgt>`_.
    """
    def __init__(self, analog: str=None, required: bool=None):
        """
        :param analog: This is the name of the NENA analog for this data.
        :type analog:  ``str``
        :param required: Does the NENA standard indicate that this data is required?
        :type required:  ``bool``
        """
        self._analog = analog
        self._required = required

    @property
    def analog(self) -> bool:
        """
        This is the name of the NENA analog for this data?
        
        :rtype: ``bool`` 
        """
        return self._analog

    @property
    def required(self) -> bool:
        """
        Does the NENA standard indicate that this data is required?
        
        :rtype: ``bool``
        """
        return self._required


class FieldInfo(object):
    """
    This class describes a field in a relation (like a table, or a feature class).
    """
    def __init__(self,
                 name: str,
                 data_type: DataType or str,
                 source: Source,
                 target: Target,
                 i18n: I18nPack,
                 unique: bool=False,
                 preferences: dict or None=None,
                 usage: Usage=None,
                 nena: NenaSpec=None,
                 domain: set or list=None):
        """  
        :param name: the field's name
        :type name:  ``str``
        :seealso: :py:func:`FieldInfo.name` 
        :param data_type: the field's data type
        :type data_type:  :py:class:`DataType` or ``str``
        :seealso: :py:func:`FieldInfo.data_type`
        :param source: information about the source from which this field's data comes
        :type source:  :py:class:`Source`
        :seealso: :py:func:`FieldInfo.source`
        :param target: information about the target data contract
        :type target:  :py:class:`Target`
        :seealso: :py:func:`FieldInfo.target`
        :param i18n: informative strings that describe the field in various languages
        :type i18n:  :py:func:`i18n.I18nPack`
        :seealso: :py:func:`FieldInfo.i18n` 
        :param unique: indicates whether or not values must be unique
        :type unique: ``bool``
        :seealso: :py:func:`FieldInfo.unique`
        :param preferences: the field's width
        :type preferences:  ``dict``
        :seealso: :py:func:`FieldInfo.width`
        :param usage: information about how the data in this field will be used
        :type usage:  :py:class:`Usage`
        :seealso: :py:func:`FieldInfo.usage`
        :param nena: information about how this field relates to the NENA standard
        :type nena:  :py:class:`NenaSpec`
        :seealso: :py:func:`FieldInfo.NenaSpec`
        :param domain: the set of legal values for the field
        :type domain:  ``set`` or ``list``
        """
        self._name = name
        self._unique = unique
        self._data_type = Enums.from_name(DataType, data_type)
        self._source = source
        self._target = target
        self._i18n = i18n
        self._preferences = preferences
        self._usage = usage if usage is not None else Usage()
        self._nena = nena if nena is not None else NenaSpec()
        self._domain = set(domain) if domain is not None else None

    @property
    def name(self) -> str:
        """
        Get the field's name.
        
        :rtype:  ``str``
        """
        return self._name

    @property
    def unique(self) -> bool:
        """
        This flag indicates whether or not the values in this field must be unique.
        
        :rtype: ``bool``
        """
        return self._unique

    @property
    def data_type(self) -> DataType:
        """
        Get the field's data type.

        :rtype:  :py:class:`DataType`
        """
        return self._data_type

    @property
    def source(self) -> Source:
        """
        Get information about the source from which the data in this field comes.
        
        :rtype: :py:class:`Source`
        """
        return self._source

    @property
    def target(self) -> Target:
        """
        Get information about the target data contract.
        
        :rtype:  :py:class:`Target` 
        """
        return self._target

    @property
    def i18n(self) -> I18nPack:
        """
        Get informative strings that describe this field in various languages.
        
        :rtype: :py:class:`I18n` 
        """
        return self._i18n

    @property
    def usage(self) -> Usage:
        """
        Get information about how this field is intended to be used.
        
        :rtype:  :py:class:`Usage` 
        """
        return self._usage

    @property
    def nena(self) -> NenaSpec:
        """
        Get information about how this field relates to the NENA specification.
        
        :rtype: :py:class:`NenaSpec`
        """
        return self._nena

    @property
    def domain(self) -> set:
        """
        Get the set of legal values for this field.
        
        :return: the set of legal values, or ``None`` if all values are acceptable
        :rtype:  ``set`` 
        """
        return self._domain

    @property
    def preferences(self) -> dict or None:
        """
        Get the field's additional preferences.
        
        :return: the field's width
        :rtype:  ``str``
        """
        return self._preferences


class Revision(object):
    """
    A "revision" contains version information about when a model was defined.
    """
    def __init__(self, title: str, sequence: int or float, author_name: str, author_email: str):
        """
        
        :param title: the revision title
        :type title:  ``str``
        :param sequence: an incrementing sequence number that may be used to order revisions sequentially
        :type sequence: ``float``
        :param author_name: the name of the format's author
        :type author_name:  ``str``
        :param author_email: the email address of the format's author
        :type author_email:  ``str``
        """
        # Grab the title before we do a little more leg work...
        self._title = title
        # If the sequence parameter is None...
        if sequence is None:
            # ...let's just start at zero.
            self._sequence = 0
        elif isinstance(sequence, numbers.Number):  # If they gave us an actual number...
            # ...great!
            self._sequence = sequence
        elif isinstance(sequence, str):  # But maybe they gave us a string, in which case...
            # ...we need to try to convert it to a number.
            try:
                self._sequence = float(sequence) if '.' in sequence else int(sequence)
            except TypeError as te:
                raise TypeError('sequence must be a number or a convertible string.') from te
        # Now let's get the other, simpler, properties.
        self._author_name = author_name
        self._author_email = author_email

    @property
    def title(self) -> str:
        """
        Get the revision's title.
        
        :return: the title
        :rtype:  ``str``
        """
        return self._title

    @property
    def sequence(self) -> int or float:
        """
        Get the revision's sequence number.

        :return: the sequence number
        :rtype:  ``int`` or ``float``
        """
        return self._sequence

    @property
    def author_name(self) -> str:
        """
        Get the name of the person who authored this revision.
        
        :return: the author's name
        :rtype:  ``str``
        """
        return self._author_name

    @property
    def author_email(self) -> str:
        """
        Get the email address of the person who authored this revision.
        
        :return: the author's email address
        :rtype:  ``str``
        """
        return self._author_email


class RelationInfo(object):
    """
    Relation information objects describe entity relations (like tables in a database).
    """
    def __init__(self,
                 name: str,
                 identity: str=None,
                 fields: List[FieldInfo]=None,
                 nena: NenaSpec=None,
                 i18n: I18nPack=None):
        """
        
        :param name: the name of the relation
        :type name:  ``str``
        :param identity: the name of the field that contains the identity value for the relation
        :type identity:  ``str``
        :seealso: :py:func:`RelationInfo.identity`
        :param fields: 
        :type fields:  ``list`` of :py:class:`FieldInfo`
        :param nena: information about how this field relates to the NENA standard
        :type nena:  :py:class:`NenaSpec`
        :param i18n: informative strings that describe the field in various languages
        :type i18n:  :py:func:`i18n.I18nPack`
        """
        self._name = name
        self._identity = identity
        # If we didn't get any fields...
        if fields is None:
            self._fields = {}  # ...our internal index is empty.
        elif isinstance(fields, list):  # If we got the type we expect...
            # ...create an index for the fields that uses the field name as a key.
            self._fields = CaseInsensitiveDict({str(field.name): field for field in fields})
        else:
            raise ValueError('common_fields must be a list.')
        self._nena = nena
        self._i18n = i18n

    @property
    def name(self) -> str:
        """
        Get the name of the relation.
        
        :rtype:  ``str``
        """
        return self._name

    @property
    def identity(self) -> str:
        """
        Get the name of the field that contains the identity values for the relation.
        
        :rtype:  ``str`` 
        """
        return self._identity

    @property
    def fields(self) -> iter:
        """
        Get this relation's field information
        
        :return:  this relation's fields
        :rtype:  iter(:py:class:`FieldInfo`)
        """
        return iter(self._fields.values())

    @property
    def i18n(self) -> I18nPack:
        """
        Get informative strings that describe this field in various languages.

        :rtype: :py:class:`I18n`
        """
        return self._i18n

    @property
    def nena(self) -> NenaSpec:
        """
        Get information about how this field relates to the NENA specification.

        :rtype: :py:class:`NenaSpec`
        """
        return self._nena
    
    def get_identity_field(self) -> FieldInfo:
        """
        Get the field information for the field that contains the identity values for the relation.
        
        :seealso: :py:func:`FieldInfo.identity`
        :rtype: :py:class:`FieldInfo`
        """
        return self.get_field(self._identity) if self._identity is not None else None

    def get_field(self, name: str) -> FieldInfo:
        """
        Get field information for the relation.
        
        :param name: the name of the relation
        :type name:  ``str``
        :return: the name of the relation
        :rtype:  :py:class:`FieldInfo`
        """
        return self._fields[name]


class FeatureTableInfo(RelationInfo):
    """
    Feature table info objects describe a feature table (*a.k.a* a "feature class").
    """
    def __init__(self,
                 name: str,
                 identity: str,
                 geometry_type: GeometryType,
                 fields: List[FieldInfo],
                 srid: int=None,
                 nena: NenaSpec=None,
                 i18n: I18nPack=None):
        """

        :param name: the name of the relation
        :type name:  ``str``
        :type identity:  ``str``
        :seealso: :py:func:`RelationInfo.identity`
        :param geometry_type: the type of geometry stored in the feature table
        :type geometry_type:  :py:class:`GeometryType`
        :param fields: the fields present in the feature table
        :type fields:  ``list`` of :py:class:`FieldInfo`
        :param srid: the spatial reference ID of geometries in this table
        :type srid:  ``int``
        :param nena: information about how this field relates to the NENA standard
        :type nena:  :py:class:`NenaSpec`
        :param i18n: informative strings that describe the field in various languages
        :type i18n:  :py:func:`i18n.I18nPack`
        """
        super().__init__(name=name, identity=identity, fields=fields, nena=nena, i18n=i18n)
        self._geometry_type = geometry_type
        self._srid = int(srid) if srid is not None else None

    @property
    def geometry_type(self) -> GeometryType:
        """
        Get the geometry type.
        
        :rtype:  :py:class:`mothergeo.geometry.GeometryType`
        """
        return self._geometry_type

    @property
    def srid(self) -> int:
        """
        Get the spatial reference ID of geometries in this table.
        
        :rtype: ``int``
        """
        # If this feature table doesn't have its own SRID, use mother's default.
        return self._srid if self._srid is not None else DEFAULT_SRID


class _RelationInfoCollection(object):
    """
    This is a base class for collections of information that define the relations (tables) in a 
    :py:class:`ModelInfo`.
    """
    def __init__(self, common_fields: List[FieldInfo], relations: List[RelationInfo], default_identity: str):
        """
        
        :param common_fields: the common fields shared among relations in this collection
        :type common_fields:  ``list`` of :py:class:`FieldInfo`
        :param relations: the relations in this collection
        :type relations:  :py:class:`RelationInfo`
        :param default_identity: the name of the default identity field for all defined relations
        :type default_identity:  ``str``
        :seealso: :py:func:`_RelationInfoCollection.default_identity`
        """
        # If we didn't get any common fields...
        if common_fields is None:
            self._common_fields = {}  # ...our internal index is empty.
        elif isinstance(common_fields, list):  # If we got the type we expect...
            # ...create an index for the fields that uses the field name as a key.
            self._common_fields = CaseInsensitiveDict({field.name: field for field in common_fields})
        else:
            raise ValueError('common_fields must be a list.')
        # If we didn't get any relations...
        if relations is None:
            self._relations = {}  # ...our internal index is empty.
        elif isinstance(relations, list):  # If we got the type we expect...
            # ...create an index for the fields that uses the table's name as a key.
            self._relations = CaseInsensitiveDict({field.name: field for field in relations})
        else:
            raise ValueError('relations must be a list.')
        self._default_identity = default_identity

    def __iter__(self):
        # Return the values in the _relations index.
        return iter(self._relations.values())

    @property
    def default_identity(self) -> str:
        """
        Get the name of the default identity field for relations in this collection.
        
        :rtype:  ``str`` 
        """
        return self._default_identity

    @property
    def common_fields(self) -> Iterator[FieldInfo]:
        """
        Get the common fields defined for the collection.

        :rtype: :py:class:`Iterator`
        """
        return iter(self._common_fields)

    def get_common_field(self, name: str) -> FieldInfo:
        """
        Get a common field from the collection.
        
        :param name: the field name
        :type name:  ``str``
        :return: the field
        :rtype:  :py:class:`FieldInfo`
        """
        if name is None:
            raise TypeError("name cannot be None.")
        elif name not in self._common_fields:
            raise KeyError("Common field '{name)' is not defined.".format(name=name))
        else:
            return self._common_fields[name]

    @property
    def relations(self) -> Iterator[RelationInfo]:
        """
        Get the relations in this collection.

        :rtype: :py:class:`Iterator[RelationInfo]`
        """
        return iter(self._relations.values())

    def get_relation(self, name: str) -> RelationInfo:
        """
        Get a relation from the collection.

        :param name: the relation's name
        :type name:  ``str``
        :return: the relation
        :rtype:  :py:class:`RelationInfo`
        """
        if name is None:
            raise TypeError('name cannot be None.')
        elif name not in self._relations:
            raise KeyError("Relation '{name)' is not defined.".format(name=name))
        else:
            return self._relations[name]

    def add_relation(self, relation: RelationInfo):
        """
        Add a relation to the collection.
        
        :param relation: the relation
        :type relation:  :py:class:`RelationInfo`
        :raises TypeError: if the argument is ``None`` 
        :raises KeyError:  if the another relation with the same name is already present
        """
        if relation is None:
            raise TypeError('relation cannot be None.')
        elif relation.name in self._relations:
            raise KeyError('The collection already contains a relation named {name}'.format(name=relation.name))
        else:
            self._relations[relation.name] = relation


class FeatureTableInfoCollection(_RelationInfoCollection):
    """
    This is a base class for collections of feature tables.
    """
    def __init__(self, common_fields, feature_tables, default_identity, common_srid=None):
        super().__init__(common_fields=common_fields, relations=feature_tables, default_identity=default_identity)
        self._common_srid = common_srid

    @property
    def common_srid(self) -> int:
        """
        Get the common spatial reference ID (SRID) shared by the relations.
        
        :return: the common SRID
        :rtype:  ``int``
        """
        # If the collection doesn't specify its own common SRID, use mother's default.
        return self._common_srid if self._common_srid is not None else DEFAULT_SRID

    def get_feature_table(self, name: str) -> FeatureTableInfo:
        """
        Get a feature table from the collection.

        :param name: the feature table's name
        :type name:  ``str``
        :return: the feature table
        :rtype:  :py:class:`FeatureTableInfo`
        :seealso: :py:func:`_RelationInfoCollection.get_relation`
        """
        return self.get_relation(name)

    @property
    def feature_tables(self) -> Iterator[FeatureTableInfo]:
        """
        Get the feature tables in this collection.

        :rtype: ``iter(:py:class:`RelationInfo`)``
        :seealso:  :py:func:`RelationInfoCollection.relations`

        .. note::

            This property returns the same values as the :py:func:`RelationInfo.relations` property.
        """
        return self.relations


class SpatialInfo(object):
    """
    Instances of this class describe the spatial elements of a model.

    :seealso: :py:class:`ModelInfo`
    """
    def __init__(self,
                 common_srid: int,
                 default_identity: str,
                 common_fields: List[FieldInfo],
                 feature_tables: FeatureTableInfoCollection):
        """

        :param common_srid: the common SRID
        :type common_srid:  ``int``
        :param default_identity: the name of the default identity field
        :type default_identity:  ``str``
        :param common_fields: field information objects that describe the fields common to all feature tables
        :type common_fields: list[:py:class:`FieldInfo`]
        :param feature_tables: the feature tables defined for the model
        :type feature_tables: :py:class:`FeatureTableInfoCollection`
        """
        self._common_srid = common_srid
        self._default_identity = default_identity
        self._common_fields = common_fields
        self._feature_tables = feature_tables

    @property
    def common_srid(self) -> int:
        """
        Get the common SRID.

        :rtype: ``int``
        """
        return self._common_srid

    @property
    def common_fields(self) -> Iterator[FieldInfo]:
        """
        Get the common fields defined for the model.

        :rtype: Iterator[FieldInfo]
        """
        return iter(self._common_fields)

    @property
    def feature_tables(self) -> FeatureTableInfoCollection:
        """
        Get the feature table information collection.

        :rtype:  :py:class:`FeatureTableInfoCollection`
        """
        return self._feature_tables

    @property
    def default_identity(self) -> str:
        """
        Get the name of the default identity column.

        :rtype: ``str``
        """
        return self._default_identity


class ModelInfo(object):
    """
    Instances of this class describe a data model.
    """
    def __init__(self, name: str, revision: Revision, spatial_info: SpatialInfo):
        """
        
        :param name: the model's name
        :type name:  ``str``
        :seealso: :py:func:`ModelInfo.name`
        :param revision: the model's revision information
        :type revision:  :py:class:`Revision`
        :seealso:  :py:func:`ModelInfo.revision`
        :param spatial_info: the model's spatial stuff
        :type spatial_info:  :py:class:`SpatialInfo`
        :seealso:  :py:func:`spatial_info`
        """
        self._name = name
        self._revision = revision
        self._spatial_info = spatial_info

    @property
    def name(self) -> str:
        """
        Get the model's name.
        
        :return: the model's name
        :rtype:  ``str``
        """
        return self._name

    @property
    def revision(self) -> Revision:
        """
        Get the model's revision information.
        
        :return: the model's revision information
        :rtype:  :py:class:`Revision`
        """
        return self._revision

    @property
    def spatial_info(self) -> SpatialInfo:
        """
        Get the model's spatial stuff.

        :return: the model's spatial stuff
        :rtype:  :py:class:`SpatialInfo`
        """
        return self._spatial_info



