#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.db.postgis.geoalchemy
.. moduleauthor:: Pat Daburu <pat@daburu.net>

How Mother works with  `GeoAlchemy <https://geoalchemy-2.readthedocs.io/en/latest/>`_.
"""

from ...codetools import Dicts
from ...geometry import GeometryType, UnsupportedGeometryException
from geoalchemy2 import Geometry
from ..modeling import DataStore, Entity, Feature, EntityClassFactory, FeatureTableClassFactory
from ...schemas.modeling import DataType, RelationInfo, FeatureTableInfo, FieldInfo
from abc import ABCMeta, abstractmethod
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

_DEFAULT_CONN_STR = 'postgresql://postgres:postgres@localhost/mother'  #: The default connection string.

Base = declarative_base()  #: The SQLAlchemy declarative base class that is the common descendant of dynamic types.


class UnsupportedDataTypeError(Exception):
    """
    An exception of this type may be raised if an unsupported :py:class:`DataType` is used.  
    """
    def __init__(self, message: str, data_type: DataType):
        """
        
        :param message: the exception message
        :type message:  ``str``
        :param data_type: the unsupported data type
        :type data_type:  :py:class:`DataType`
        """
        super().__init__(message)
        self._data_type = data_type

    @property
    def data_type(self) -> DataType:
        """
        Get the unsupported data type.
        
        :rtype: :py:class:`DataType` 
        """
        return self._data_type


class GeoAlchemyEntity(Entity):
    """
    This is an abstract class that can be extended dynamically to create new entity class types.
    """
    __metaclass__ = ABCMeta
    __self_properties = [
        '_geoalchemy_obj',
        '_geoalchemy_class',
        '_data_store'
    ]  #: These are the properties that are never deferred to the encapsulated GeoAlchemy object.

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._geoalchemy_obj = self._geoalchemy_class(**kwargs)

    def __getattr__(self, item):
        # If the requested property is one of this object's properties (that is to say, it's _not_ a property of
        # the encapsulated GeoAlchemy object)...
        if item in self.__self_properties:
            # ...go straight to this instance's dictionary to retrieve the value.
            return self.__dict__[item]
        else:
            # Otherwise, retrieve the value from the encapsulated GeoAlchemy object.
            return getattr(self._geoalchemy_obj, item)

    def __setattr__(self, key, value):
        # If the requested property is one of this object's properties (that is to say, it's _not_ a property of
        # the encapsulated GeoAlchemy object)...
        if key in self.__self_properties:
            # ...go straight to this instance's dictionary to retrieve the value.
            self.__dict__[key] = value
        else:
            # Otherwise, retrieve the value from the encapsulated GeoAlchemy object.
            setattr(self._geoalchemy_obj, key, value)


class GeoAlchemyFeature(Feature, GeoAlchemyEntity):
    """
    This is an abstract class that can be extended dynamically to create new feature class class types.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GeoAlchemyDataStore(DataStore):
    """
    Instances of this class contain references to important GeoAlchemy hooks, like the current
    engine and session.
    """

    def __init__(self, engine: Engine, session: Session, schema: str = 'public'):
        """

        :param engine: the GeoAlchemy engine
        :type engine:  :rtype: :py:class:`sqlalchemy.engine.Engine`
        :param session: the GeoAlchemy session
        :type session:  :rtype: `:py:class:`sqlalchemy.orm.session.Session`
        :param schema: the name of the preferred PostgreSQL schema
        :type schema:  ``str``
        :seealso: :py:func:`engine`
        :seealso: :py:func:`session`
        :seealso: :py:func:`schema`
        """
        super().__init__()
        self._engine = engine
        self._session = session
        self._schema = schema

    @property
    def engine(self) -> Engine:
        """
        Get the GeoAlchemy engine.

        :rtype: :py:class:`sqlalchemy.engine.Engine`
        """
        return self._engine

    @property
    def session(self) -> Session:
        """
        Get the GeoAlchemy session.

        :rtype: :py:class:`sqlalchemy.orm.session.Session`
        """
        return self._session

    @property
    def schema(self) -> str:
        """
        Get the name of the preferred PostgreSQL schema.

        :rtype: ``str``
        """
        return self._schema

    def add(self, entity: GeoAlchemyEntity):
        self.session.add(entity)

    def commit(self):
        self.session.commit()

    @staticmethod
    def create(connection_string: str = _DEFAULT_CONN_STR) -> DataStore:
        """
        Create a :py:class:`GeoAlchemyDataStore` from a PostgreSQL connection string.

        :param connection_string: a PostgreSQL data_store variable.
        :type connection_string:  ``str``
        :rtype: :py:class:`GeoAlchemyDataStore`
        """
        engine = create_engine(connection_string, echo=False)
        session = sessionmaker(bind=engine)()
        return GeoAlchemyDataStore(engine=engine, session=session)


# def create_environment(connection_string: str = _DEFAULT_CONN_STR) -> GeoAlchemyDataStore:
#     """
#     Create a :py:class:`GeoAlchemyDataStore` from a PostgreSQL connection string.
#
#     :param connection_string: a PostgreSQL data_store variable.
#     :type connection_string:  ``str``
#     :rtype: :py:class:`GeoAlchemyDataStore`
#     """
#     engine = create_engine(connection_string, echo=False)
#     session = sessionmaker(bind=engine)()
#     return GeoAlchemyDataStore(engine=engine, session=session)


class _DataTypeDefaults(object):
    """
    This is a set of internal constants that represent default options for different data types.
    """
    text_length = 150  #: the default length of a text column


class GeoAlchemyEntityClassFactory(EntityClassFactory):
    """
    Extend this class to create utility classes that can turn a :py:class:`RelationInfo` instance into an entity.
    """
    __metaclass__ = ABCMeta

    def __init__(self, data_store: GeoAlchemyDataStore, geometry_column_name: str= 'geom'):
        """

        :param data_store: the GeoAlchemy data store
        :type data_store:  :py:class:`GeoAlchemyDataStore`
        """
        super().__init__()
        if data_store is None:
            raise TypeError('data_store parameter may not be None.')
        self._data_store = data_store
        self._geometry_column_name = geometry_column_name

    @property
    def data_store(self) -> GeoAlchemyDataStore:
        """
        Get the data store this class factory is using.

        :rtype: :py:class:`GeoAlchemyDataStore`
        """
        return self._data_store

    @property
    def geometry_column_name(self) -> str:
        """
        Get the name of the field that will contain geometries.

        :rtype: ``str``
        """
        return self._geometry_column_name

    def make(self, relation_info: RelationInfo, schema: str='public') -> type:
        """
        Define a new :py:class:`GeoAlchemyEntity` class based on the definition in a :py:class:`RelationInfo`.

        :param relation_info: the relation information that defines the entity
        :type relation_info:  :py:class:`RelationInfo`
        :param schema: the PostgreSQL schema
        :type schema:  ``str``
        :rtype: ``type``
        :return: a new class extended from :py:class:`GeoAlchemyEntity`
        :seealso: :py:func:`GeoAlchemyDataStore.schema`
        """
        # Let's figure out what schema we're working in.
        _schema = schema if schema is not None else self.data_store.schema
        # Let's start building up the new class' properties.
        _table_props = {
            "__tablename__": relation_info.name,
            "__table_args__": {"schema": _schema}
        }
        # Define the field properties we need to construct the class.
        _field_props = self._define_fields(relation_info=relation_info)
        # Merge the table properties and the field properties.
        props = {**_table_props, **_field_props}
        # We should now have enough information to construct the GeoAlchemy type.
        inner_cls = type(
            "GeoAlchemyDynamic_{relation_name}_Inner".format(relation_name=relation_info.name),
            (Base,),  # Inherit from the SQLAlchemy declarative base class.
            props)  # Provide the properties.
        # Create the GeoAlchemy table in the database.
        inner_cls.__table__.create(self.data_store.engine)
        # Now let's create the wrapper class.
        new_cls = type(
            "GeoAlchemyDynamic_{relation_name}".format(relation_name=relation_info.name),
            (self.base_type,),  # Inherit from the type specified by the factory.
            {
                '_geoalchemy_class': inner_cls,
                '_data_store': self._data_store  # Each instance will have a reference to the data_store.
            }
        )
        # That's it!
        return new_cls

    @property
    def base_type(self):
        """
        This is the base type for any new types created by this factory.  Override this property if your factory
        needs to specify a different base type.
        
        :return: the base type
        :rtype:  ``type`` (:py:class:`GeoAlchemyEntity`)
        """
        return GeoAlchemyEntity

    def _define_fields(self, relation_info: RelationInfo) -> dict:
        """
        This is a template method that creates a dictionary of properties that will be used in the construction of
        a new type.  Override this method to modify the properties of the new type before it is created.
        
        :param relation_info: the relation information from which properties are constructed
        :type relation_info:  :py:class:`RelationInfo`
        :return: the properties to add to the new type
        :rtype:  ``dict``
        """
        # Let's use a dictionary comprehension to construct the properties dict.
        return {
            # The property name is the same as the field name.
            str(field.name):
                # The SqlAlchemy column will be created by the factory method.
                self._field_info_to_sqlalchemy_column(
                    field_info=field,
                    identity=(relation_info.get_identity_field() == field))
            for field in relation_info.fields
        }

    @staticmethod
    def _field_info_to_sqlalchemy_column(field_info: FieldInfo, identity: bool=False) -> Column:
        """
        Create a SQLAlchemy ``Column`` based on the information in a :py:class:`FieldInfo` object.
        
        :param field_info: the field information
        :type field_info:  :py:class:`FieldInfo`
        :param identity: Is this the identity column (i.e. the primary key)?
        :type identity:  ``bool``
        :return: the SQLAlchemy column
        :rtype:  :py:class:`sqlalchemy.Column`
        """
        # What's the name of the column?
        column_name = field_info.name
        # Grab the preferences from the field information (which may, or may not, have any).
        preferences = field_info.preferences if field_info.preferences is not None else {}
        # And to make the following code a little shorter, let's reference the data type directly.
        data_type = field_info.data_type
        # The next step is to create a GeoAlchemy column type suitable to the data type.
        if data_type == DataType.TEXT:  # Text?
            # How big can this string be?
            length = Dicts.try_get(preferences, 'length', default=_DataTypeDefaults.text_length).value
            # Great.  Create the column.
            column = Column(column_name, String(length=length), primary_key=identity)
        # TODO: We have to figure out how to handle GUIDS.
        # elif field_info.data_type == DataType.UUID:  # UUID? (i.e Guid?)
        #     column = None
        elif data_type == DataType.INT:  # Integer?
            column = Column(column_name, Integer, primary_key=identity)
        elif data_type == DataType.FLOAT:  # Floating point number?
            column = Column(column_name, Float, primary_key=identity)
        elif data_type == DataType.DATETIME:  # DateTime?
            column = Column(column_name, DateTime, primary_key=identity)
        else:
            # We didn't find anything we can use.
            raise UnsupportedDataTypeError(
                message='The {dt} data type is unsupported.'.format(dt=data_type.name),
                data_type=data_type)
        # Return what we have.
        return column


class GeoAlchemyFeatureTableClassFactory(GeoAlchemyEntityClassFactory, FeatureTableClassFactory):
    """
    Extend this class to create utility classes that can turn a :py:class:`FeatureTableInfo` instance into an feature.
    """

    def __init__(self, data_store: GeoAlchemyDataStore):
        """

        :param data_store: the GeoAlchemy data_store
        :type data_store:  :py:class:`GeoAlchemyDataStore`
        """
        GeoAlchemyEntityClassFactory.__init__(self, data_store)

    @property
    def base_type(self):
        """
        This is the base type for any new types created by this factory.  Override this property if your factory
        needs to specify a different base type.

        :return: the base type
        :rtype:  ``type`` (:py:class:`GeoAlchemyFeature`)
        """
        return GeoAlchemyFeature

    def _define_fields(self, relation_info: FeatureTableInfo) -> dict:
        """
        This is a template method that creates a dictionary of properties that will be used in the construction of
        a new type.  Override this method to modify the properties of the new type before it is created.

        :param relation_info: the feature table information from which properties are constructed
        :type relation_info:  :py:class:`FeatureTableInfo`
        :return: the properties to add to the new type
        :rtype:  ``dict``
        """
        # Get the properties from the parent class.
        props = super()._define_fields(relation_info=relation_info)
        # Add the geometry type.
        props['geom'] = self._geometry_type_to_sqlalchemy_column(relation_info.geometry_type)
        # Return the dictionary.
        return props

    def _geometry_type_to_sqlalchemy_column(self, geometry_type: GeometryType) -> Column:
        """
        Create a SQLAlchemy ``Column`` for a supported :py:class:`GeometryType`.

        :param geometry_type: the geometry type
        :type geometry_type:  :py:class:`GeometryType`
        :return: the SQLAlchemy column
        :rtype:  :py:class:`sqlalchemy.Column`
        """
        if geometry_type == GeometryType.POINT:
            return Column(self.geometry_column_name, Geometry('POINT'))
        elif geometry_type == GeometryType.POLYLINE:
            return Column(self.geometry_column_name, Geometry('POLYLINE'))
        elif geometry_type == GeometryType.POLYGON:
            return Column(self.geometry_column_name, Geometry('POLYGON'))
        else:  # It looks like we didn't account for this geometry type.
            raise UnsupportedGeometryException(
                message="The geometry type is not supported.",
                geometry_type=geometry_type)












# class SessionOptions(object):
#     def __init__(self,
#                  connection_string: str='postgresql://postgres:postgres@localhost/mother'):
#         self.connection_string = connection_string  #: This is the PostgreSQL/PostGIS connection string.
#
#
# class Session(object):
#     def __init__(self, options: SessionOptions=None):
#         # If we didn't get any actual options, use a default.
#         self._options = options if options is not None else SessionOptions()
#         # Get the engine from the options (or create a new one).
#         self._geoalchemy_engine = create_engine(options.connection_string, echo=True)
#         # Create the session object.
#         self._geoalchemy_session = sessionmaker(bind=self._engine)()
#
#     def create_table(self, geoalchemy_table):
#         geoalchemy_table.create(self._geoalchemy_engine)
#
#     def drop_table(self, geoalchemy_table):
#         geoalchemy_table.drop(self._geoalchemy_engine)
#
#     def add_entity(self, geoalchemy_entity):
#         self._geoalchemy_session.add(geoalchemy_entity)
#
#     def commit(self):
#         self._geoalchemy_session.commit()
#
#
# class SessionManager(object):
#
#     def __init__(self):
#         # The default session is just a session.
#         self._default_session = Session()  #: This is the default session. # TODO: Use configuration!
#         # Sessions other than the default session are indexed by name in a case-insensitive dictionary.
#         self._other_sessions = CaseInsensitiveDict({})
#
#     def get_session(self, name: str=None):
#         if name is None:
#             return self._default_session
#         else:
#             return self._other_sessions[name]
#
#     def create_session(self, name: str, options: SessionOptions, overwrite: bool=False):
#         # Let's make sure we aren't about to clobber an existing session (unless the caller has expressly asked us
#         # do that).
#         if not overwrite and name in self._other_sessions:
#             raise KeyError('Another session named {name} already exists.'.format(name=name))
#         # Create the new session based on the options we got from the caller.
#         session = Session(options=options)
#         # Stash it in the dictionary.
#         self._other_sessions[name] = session
#         # We're good to go.
#         return session



