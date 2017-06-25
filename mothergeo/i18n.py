#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.i18n
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Think locally, act globally.  These are tools to help with internationalization.
"""

from collections import UserDict
from typing import Dict

current_locale = None  #: The current locale (``None`` indicates the default locale.)


class I18nPack(UserDict):
    """
    This is a dictionary of translatable strings.
    
    :Example:
    
    >>> pack = I18nPack({
            'alpha': 'apple',
            'beta': 'banana',
            'gamma': 'grapes'
        })
    >>> pack.add_translation('alpha', '林檎', 'ja_jp')
    >>> pack.add_translation('beta', 'バナナ', 'ja_jp')
    
    .. seealso:: :py:func:`I18nPack.add_translation`
    """
    def __init__(self, initialdata: dict=None):
        """

        :param initialdata: a dictionary you can use to seed this package
        :type initialdata:  ``dict``
        """
        super().__init__(initialdata if initialdata is not None else {})
        self.__translations = {}  #: This is a dictionary of locale's to translation packs.

    def add_translation(self, key: str, translation: str, locale: str=None):
        """
        Add a translation to this package.
        
        :param key: the key used to retrieve the translated value
        :type key:  ``str``
        :param translation: the translation you want people to read
        :type translation:  ``str``
        :param locale: the locale in which the translation can be understood
        :type locale:  ``str``
        """
        # If no locale is specified...
        if locale is None:
            # ...we're using the default.
            pack = self
        elif locale in self.__translations:  # A locale was specified, and we have a pack for it, so...
            # ...we're going to be using it.
            pack = self.__translations[locale]
        else:  # This is our first encounter with this pack, so...
            # ...create a new one.
            pack = I18nPack()
            # Now add it to the collection of translations.
            self.__translations[locale] = pack
        # Now that we have a pack to update, let's do so.
        pack[key] = translation

    def set_translations(self, translations: Dict[str, str], locale: str=None):
        """
        Update the pack with a complete set of translations.
        
        :param translations: the translations for the specified locale
        :type translations:  ``dict[str, str]``
        :param locale: the locale in which the translations would be understood (or ``None`` to set the defaults)
        :type locale:  ``str``
        :raises ValueError: if translations is not a ``dict``
        """
        # Make sure we're getting a dictionary of translations with which we can work.
        if not isinstance(translations, dict):
            raise ValueError('{arg} must be of type {type}'.format(arg='translations', type=dict))
        # If no no locale is specified (or if the caller is explicitly telling us to set the defaults)...
        if locale is None or locale == 'default':
            # ...we're changing the values in the dictionary.
            self.clear()
            for key in translations.keys():
                self[key] = translations[key]
        else:  # Otherwise, insert (or swap) the previous dictionary.
            self.__translations[locale] = I18nPack(translations)

    def __getattr__(self, name):
        # Let's figure out which pack we're supposed to be looking in.
        pack = self.__translations[current_locale] \
            if current_locale is not None and current_locale in self.__translations \
            else self
        # If the name is defined in the pack...
        if name in pack:
            return pack[name]  # ...great!
        elif pack is not self and name in self:  # If it's not defined in the pack, but may be in the defaults...
            return self[name] # ...return the default.
        else: # We just couldn't find it.  C'est la vie.
            return None






