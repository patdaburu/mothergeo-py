#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
import mothergeo.i18n
from mothergeo.schemas.modeling import DataType, Requirement
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
        self.assertIsNone(source.requirement)

    def test_json_2_target_without_values(self):
        jsons = '{}'
        jsobj = json.loads(jsons)
        target = JsonModelInfoParser._json_2_target(jsobj)
        self.assertFalse(target.calculated)
        self.assertFalse(target.guaranteed)

    def test_json_2_target_with_values(self):
        jsons = """
        {
          "calculated": true,
          "guaranteed": true
        }
        """
        jsobj = json.loads(jsons)
        target = JsonModelInfoParser._json_2_target(jsobj)
        self.assertTrue(target.calculated)
        self.assertTrue(target.guaranteed)

    def test_json_2_usage_without_values(self):
        jsons = '{}'
        jsobj = json.loads(jsons)
        usage = JsonModelInfoParser._json_2_usage(jsobj)
        self.assertFalse(usage.search)
        self.assertFalse(usage.display)

    def test_json_2_usage_with_values(self):
        jsons = """
        {
          "search": true,
          "display": true
        }
        """
        jsobj = json.loads(jsons)
        usage = JsonModelInfoParser._json_2_usage(jsobj)
        self.assertTrue(usage.search)
        self.assertTrue(usage.display)

    def test_json_2_nena_spec_without_values(self):
        jsons = '{}'
        jsobj = json.loads(jsons)
        nena_spec = JsonModelInfoParser._json_2_nena_spec(jsobj)
        self.assertIsNone(nena_spec.analog)
        self.assertFalse(nena_spec.required)

    def test_json_2_nena_spec_with_values(self):
        jsons = """
        {
          "analog": "NENA_DEFINED_FIELD",
          "required": true
        }
        """
        jsobj = json.loads(jsons)
        nena_spec = JsonModelInfoParser._json_2_nena_spec(jsobj)
        self.assertEqual("NENA_DEFINED_FIELD", nena_spec.analog)
        self.assertTrue(nena_spec.required)

    def test_json_2_field_info_with_all_values(self):
        jsons = """
        {
            "name": "srcFullNam",
            "unique": true,
            "type": "text",
            "width": 200,
            "source": {
              "requirement" : "required",
              "analogs" : [ "street_nam?", "strnam" ]
            },
            "target": {
              "calculated": true,
              "guaranteed": false
            },
            "usage": {
              "search": true,
              "display": false
            },
            "nena": {
              "analog": "TEST_NENA_ANALOG",
              "required": true
            },
            "i18n": {
              "default": {
                "friendlyName": "I18N_FRIENDLY",
                "description": "I18N_DESC"
              },
              "ja_jp": {
                "friendlyName": "プレースホルダ",
                "description": "プレースホルダの説明"
              }
            }
          }
        """
        jsobj = json.loads(jsons)
        field_info = JsonModelInfoParser._json_2_field_info(jsobj)
        self.assertEqual('srcFullNam', field_info.name)
        self.assertEqual(True, field_info.unique)
        self.assertEqual(DataType.TEXT, field_info.data_type)
        self.assertEqual(200, field_info.width)
        self.assertEqual(Requirement.REQUIRED, field_info.source.requirement)
        self.assertEqual(2, len(field_info.source.analogs))
        self.assertTrue('street_nam?' in field_info.source.analogs)
        self.assertTrue('strnam' in field_info.source.analogs)
        self.assertTrue(field_info.target.calculated)
        self.assertFalse(field_info.target.guaranteed)
        self.assertTrue(field_info.usage.search)
        self.assertFalse(field_info.usage.display)
        self.assertEqual('TEST_NENA_ANALOG', field_info.nena.analog)
        self.assertTrue(field_info.nena.required)
        self.assertEqual('I18N_FRIENDLY', field_info.i18n.friendlyName)
        self.assertEqual('I18N_DESC', field_info.i18n.description)


if __name__ == '__main__':
    unittest.main()
