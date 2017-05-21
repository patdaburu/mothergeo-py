#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
import mothergeo.i18n
from mothergeo.schemas.modeling import Requirement
from mothergeo.schemas.parsing import JsonModelInfoParser


class TestJsonModelInfoParser(unittest.TestCase):

    def test_json_2_revision(self):
        jsons = """
        {
            "title": "The Title",
            "sequence": 1234567,
            "authorName": "Pat Blair",
            "authorEmail": "pat@daburu.net"
        }
        """
        jsobj = json.loads(jsons)
        revision = JsonModelInfoParser._json_2_revision(jsobj)
        self.assertEqual(revision.title, 'The Title')
        self.assertEqual(revision.sequence, 1234567)
        self.assertEqual(revision.author_name, 'Pat Blair')
        self.assertEqual(revision.author_email, 'pat@daburu.net')

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

    def test_json_2_source_required(self):
        jsons = """
        {
          "requirement" : "required"
        }
        """
        jsobj = json.loads(jsons)
        source = JsonModelInfoParser._json_2_source(jsobj)
        self.assertEqual(Requirement.REQUIRED, source.requirement)

    def test_json_2_source_no_requirement(self):
        jsons = '{}'
        jsobj = json.loads(jsons)
        source = JsonModelInfoParser._json_2_source(jsobj)
        self.assertEqual(None, source.requirement)

    def test_json_2_target_without_values(self):
        jsons = '{}'
        jsobj = json.loads(jsons)
        target = JsonModelInfoParser._json_2_target(jsobj)
        self.assertEqual(False, target.calculated)
        self.assertEqual(False, target.guaranteed)

    def test_json_2_target_with_values(self):
        jsons = """
        {
          "calculated": true,
          "guaranteed": true
        }
        """
        jsobj = json.loads(jsons)
        target = JsonModelInfoParser._json_2_target(jsobj)
        self.assertEqual(True, target.calculated)
        self.assertEqual(True, target.guaranteed)


if __name__ == '__main__':
    unittest.main()
