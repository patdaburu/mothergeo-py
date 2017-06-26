#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.config
.. moduleauthor:: Pat Daburu <pat@daburu.net>

May I take your order, please?
"""

import os
from configparser import ConfigParser


class ConfigurationManager(object):
    """
    Use a configuration manager to keep track of the configurable aspects of the system.
    """
    def __init__(self):
        # Create the built-in Python configuration parser we'll use to read configuration in from a file.
        self._config_parser = ConfigParser()
        # It's possible for environment variables to override values configured elsewhere.  This is how we'll keep
        # track of what overrides what.
        self._env_overrides = {}

    def load(self, config_info: str):
        """
        Load configuration information.
        
        :param config_info: the configuration information (most likely a path to a file or something similar)
        :type config_info:  ``str``
        """
        self._config_parser.read(config_info)

    def get(self, section: str, option: str, fallback: str=None) -> str or None:
        """
        Get a configured value.
        
        :param section: the name of the configuration section
        :type section:  ``str``
        :param option: the name of the configuration option
        :type option:  ``str``
        :param fallback: the value to return if no configured value is found
        :type fallback:  ``str``
        :return: the configured value
        :rtype:  ``str``
        """
        # Check to see if there are environment variables that are supposed to override this option.
        env_override_key = ConfigurationManager._to_dict_key(section=section, option=option)
        # If we do have an override, and the mapped environment variable seems to be configured in the environment...
        if env_override_key in self._env_overrides and self._env_overrides[env_override_key] is os.environ:
            # ...return the environment variable's value.
            return os.environ[self._env_overrides[env_override_key]]
        else:
            # Otherwise, see what the built-in Python configuration parser has.
            return self._config_parser.get(section=section, option=option, fallback=fallback)

    def map_env_variable(self, section: str, option: str, env_var: str):
        """
        
        :param section: 
        :param option: 
        :param env_var: 
        :return: 
        """
        # Create a key to use in the environment variable overrides dictionary.
        key = ConfigurationManager._to_dict_key(section=section, option=option)
        # Now, let's set up the mapping.
        self._env_overrides[key] = env_var

    def set(self, section: str, option: str, value: str):
        """
        Set a configuration value.
        
        :param section: 
        :type section:
        :param option:
        :type option:
        :param value:
        :type value:
        :return: 
        :rtype:
        """
        self._config_parser.set(section=section, option=option, value=value)

    @staticmethod
    def _to_dict_key(section: str, option: str) -> tuple(str or None, str or None):
        """
        Create a dictionary key from a configuration section name and option.
        :param section: the configuration section
        :type section:  ``str``
        :param option: the configuration option name
        :type option:  ``str`` 
        :return: a key based upon the argument values, suitable for use in a dictionary
        :rtype:  ``tuple(str or None, str or None)``
        """
        # Create a tuple key based on the section and option.
        key = (str.lower(section) if section is not None else None,
               str.lower(option) if option is not None else None)
        return key

