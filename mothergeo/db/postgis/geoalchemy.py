#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.db.postgis.geoalchemy
.. moduleauthor:: Pat Daburu <pat@daburu.net>

How Mother works with  `GeoAlchemy <https://geoalchemy-2.readthedocs.io/en/latest/>`_.
"""

from ..modeling import Entity, Feature, EntityClassFactory, FeatureTableClassFactory
from ...schemas.modeling import RelationInfo, FeatureTableInfo, FieldInfo
from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

_DEFAULT_CONN_STR = 'postgresql://postgres:postgres@localhost/mother'  #: The default connection string.


class GeoAlchemyEnvironment(object):
    """
    Instances of this class contain references to important GeoAlchemy hooks, like the current 
    engine and session.
    """
    def __init__(self, engine: Engine, session: Session):
        """
        
        :param engine: the GeoAlchemy engine
        :type engine:  :rtype: :py:class:`sqlalchemy.engine.Engine`
        :param session: the GeoAlchemy session
        :type session:  :rtype: `:py:class:`sqlalchemy.orm.session.Session`
        :seealso: :py:func:`engine`
        :seealso: :py:func:`session`
        """
        self._engine = engine
        self._session = session

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


class GeoAlchemyEntity(Entity):
    """
    This is an abstract class that can be extended dynamically to create new entity class types.
    """
    __metaclass__ = ABCMeta
    __self_properties__ = [
        '_geoalchemy_obj',
        '__geoalchemy_class__'
    ]  #: These are the properties that are never deferred to the encapsulated GeoAlchemy object.

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__()
        self._geoalchemy_obj = self.__geoalchemy_class__(**kwargs)

    def __getattr__(self, item):
        # If the requested property is one of this object's properties (that is to say, it's _not_ a property of
        # the encapsulated GeoAlchemy object)...
        if item in self.__self_properties__:
            # ...go straight to this instance's dictionary to retrieve the value.
            return self.__dict__[item]
        else:
            # Otherwise, retrieve the value from the encapsulated GeoAlchemy object.
            return getattr(self._geoalchemy_obj, item)

    def __setattr__(self, key, value):
        # If the requested property is one of this object's properties (that is to say, it's _not_ a property of
        # the encapsulated GeoAlchemy object)...
        if key in self.__self_properties__:
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


def create_environment(connection_string: str = _DEFAULT_CONN_STR) -> GeoAlchemyEnvironment:
    """
    Create a :py:class:`GeoAlchemyEnvironment` from a PostgreSQL connection string.
    
    :param connection_string: a PostgreSQL environment variable.
    :type connection_string:  ``str``
    :rtype: :py:class:`GeoAlchemyEnvironment`
    """
    engine = create_engine(connection_string, echo=False)
    session = sessionmaker(bind=engine)
    return GeoAlchemyEnvironment(engine=engine, session=session)


# class GeoAlchemyEntityClassFactory(EntityClassFactory):
#     """
#     Extend this class to create utility classes that can turn a :py:class:`RelationInfo` instance into an entity.
#     """
#     __metaclass__ = ABCMeta
#
#     def __init__(self, environment: GeoAlchemyEnvironment):
#         """
#
#         :param environment: the GeoAlchemy environment
#         :type environment:  :py:class:`GeoAlchemyEnvironment`
#         """
#         if environment is None:
#             raise TypeError('environment parameter may not be None.')
#         self._environment = environment
#
#     @property
#     def environment(self) -> GeoAlchemyEnvironment:
#         """
#         Get the environment this class factory is using.
#
#         :rtype: :py:class:`GeoAlchemyEnvironment`
#         """
#         return self._environment
#
#     @abstractmethod
#     def make(self, relation_info: RelationInfo) -> type:
#         """
#         Define a new :py:class:`GeoAlchemyEntity` class based on the definition in a :py:class:`RelationInfo`.
#
#         :param relation_info: the relation information that defines the entity
#         :rtype: ``type``
#         :return: a new class extended from :py:class:`GeoAlchemyEntity`
#         """
#         pass


# class GeoAlchemyFeatureTableClassFactory(EntityClassFactory, FeatureTableClassFactory):
#     """
#     Extend this class to create utility classes that can turn a :py:class:`FeatureTableInfo` instance into an feature.
#     """
#
#     def make(self, relation_info: FeatureTableInfo) -> type:
#         """
#         Define a new :py:class:`GeoAlchemyFeature` subclass based on the definition in a :py:class:`FeatureTableInfo`.
#
#         :param relation_info: the relation information that defines the entity
#         :rtype: ``type``
#         :return: a new class extended from :py:class:`GeoAlchemyFeatureTable`
#         """
#         pass

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



