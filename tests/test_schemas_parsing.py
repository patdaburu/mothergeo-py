#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
import mothergeo.i18n
from mothergeo.schemas.parsing import JsonModelInfoParser


class TestJsonModelInfoParser(unittest.TestCase):

    def test_json_2_i18n(self):
        jsons = """
        {
          "default": {
            "friendlyName": "A Friendly Name",
            "description": "A friendly thing is friendly."
          },
          "ja_jp": {
            "friendlyName": "プレースホルダ",
            "description": "プレースホルダの説明"
          }
        }
        """
        jsobj = json.loads(jsons)
        pack = JsonModelInfoParser._json_2_i18n(jsobj)
        self.assertEqual(pack.friendlyName, 'A Friendly Name')
        self.assertEqual(pack.description, 'A friendly thing is friendly.')
        # Get the current locale so we can reset it when we're finished here.
        original_locale = mothergeo.i18n.current_locale
        mothergeo.i18n.current_locale = 'ja_jp'
        self.assertEqual(pack.friendlyName, 'プレースホルダ')
        self.assertEqual(pack.description, 'プレースホルダの説明')
        mothergeo.i18n.current_locale = original_locale

if __name__ == '__main__':
    unittest.main()
