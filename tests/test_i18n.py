#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mothergeo.i18n
from mothergeo.i18n import I18nPack


class TestI18nPack(unittest.TestCase):

    def setUp(self):
        # Store the current locale so we can set it back when we tear down.
        self._original_locale = mothergeo.i18n.current_locale

    def tearDown(self):
        # Restore the current locale.
        mothergeo.i18n.current_locale = self._original_locale

    def test_init_with_initialdata(self):
        pack = I18nPack({
            'alpha': 'apple',
            'beta': 'banana',
            'gamma': 'grapes'
        })
        self.assertEqual(pack.alpha, 'apple')
        self.assertEqual(pack.beta, 'banana')
        self.assertEqual(pack.gamma, 'grapes')

    def test_add_translation_without_locale(self):
        pack = I18nPack()
        pack.add_translation('alpha', 'apple')
        pack.add_translation('beta', 'banana')
        pack.add_translation('gamma', 'grapes')
        self.assertEqual(pack.alpha, 'apple')
        self.assertEqual(pack.beta, 'banana')
        self.assertEqual(pack.gamma, 'grapes')

    def test_add_translation_with_locale(self):
        pack = I18nPack()
        pack.add_translation('alpha', 'apple')
        pack.add_translation('beta', 'banana')
        pack.add_translation('gamma', 'grapes')
        pack.add_translation('alpha', '林檎', 'ja_jp')
        pack.add_translation('beta', 'バナナ', 'ja_jp')
        mothergeo.i18n.current_locale = 'ja_jp'
        try:
            self.assertEqual(pack.alpha, '林檎')
            self.assertEqual(pack.beta, 'バナナ')
            self.assertEqual(pack.gamma, 'grapes')
        finally:
            mothergeo.i18n.current_locale = None
        self.assertEqual(pack.alpha, 'apple')
        self.assertEqual(pack.beta, 'banana')
        self.assertEqual(pack.gamma, 'grapes')

    def test_set_translations_without_locale(self):
        pack = I18nPack()
        pack.set_translations(translations={
            'alpha': 'apple',
            'beta': 'banana',
            'gamma': 'grapes'
        })
        self.assertEqual(pack.alpha, 'apple')
        self.assertEqual(pack.beta, 'banana')
        self.assertEqual(pack.gamma, 'grapes')

    def test_set_translations_with_locale(self):
        pack = I18nPack()
        # Set the default translations.
        pack.set_translations(translations={
            'alpha': 'apple',
            'beta': 'banana',
            'gamma': 'grapes'
        }, locale='default')  # For this test, we'll cover the branch that checks specifically for locale='default'.
        # Set the translations for a specific locale.
        pack.set_translations(translations={
            'alpha': '林檎',
            'beta': 'バナナ'
        }, locale='ja_jp')
        mothergeo.i18n.current_locale = 'ja_jp'
        try:
            self.assertEqual(pack.alpha, '林檎')
            self.assertEqual(pack.beta, 'バナナ')
            self.assertEqual(pack.gamma, 'grapes')
        finally:
            mothergeo.i18n.current_locale = None
        self.assertEqual(pack.alpha, 'apple')
        self.assertEqual(pack.beta, 'banana')
        self.assertEqual(pack.gamma, 'grapes')

if __name__ == '__main__':
    unittest.main()




