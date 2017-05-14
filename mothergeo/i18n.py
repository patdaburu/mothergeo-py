#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.i18n
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Think locally, act globally.  These are tools to help with internationalization.
"""

from collections import UserDict

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
    def __init__(self, initialdata=None, locale=None):
        """

        :param initialdata: a dictionary you can use to seed this package
        :type initialdata:  ``dict``
        :param locale: the locale in which the values in this package can be understood
        :type locale:  ``str``
        """
        super().__init__(initialdata if initialdata is not None else {})
        self._translations = {}  #: This is a dictionary of locale's to translation packs.
        self._locale = locale  #: The locale to which these values are appropriate.

    def add_translation(self, key, translation, locale=None):
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
        elif locale in self._translations:  # A locale was specified, and we have a pack for it, so...
            # ...we're going to be using it.
            pack = self._translations[locale]
        else:  # This is our first encounter with this pack, so...
            # ...create a new one.
            pack = I18nPack(locale=locale)
            # Now add it to the collection of translations.
            self._translations[locale] = pack
        # Now that we have a pack to update, let's do so.
        pack[key] = translation

    def __getattr__(self, name):
        # Let's figure out which pack we're supposed to be looking in.
        pack = self._translations[current_locale] \
            if current_locale is not None and current_locale in self._translations \
            else self
        # If the name is defined in the pack...
        if name in pack:
            return pack[name]  # ...great!
        elif pack is not self and name in self:  # If it's not defined in the pack, but may be in the defaults...
            return self[name] # ...return the default.
        else: # We just couldn't find it.  C'est la vie.
            return None






