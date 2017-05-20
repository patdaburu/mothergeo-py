#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mothergeo.schemas.modeling import Requirement, Revision, Source


class TestRevision(unittest.TestCase):

    def test_init_sequence_is_num(self):
        revision = Revision(title='Test Title',
                            sequence=1,
                            author_name='Eric Blair',
                            author_email='eb1984@gmail.com')
        self.assertEqual('Test Title', revision.title)
        self.assertEqual(1, revision.sequence)
        self.assertEqual('Eric Blair', revision.author_name)
        self.assertEqual('eb1984@gmail.com', revision.author_email)

    def test_init_sequence_is_int_str(self):
        revision = Revision(title='Test Title',
                            sequence='100',
                            author_name='Eric Blair',
                            author_email='eb1984@gmail.com')
        self.assertEqual('Test Title', revision.title)
        self.assertEqual(100, revision.sequence)
        self.assertEqual('Eric Blair', revision.author_name)
        self.assertEqual('eb1984@gmail.com', revision.author_email)

    def test_init_sequence_is_float_str(self):
        revision = Revision(title='Test Title',
                            sequence='100.1',
                            author_name='Eric Blair',
                            author_email='eb1984@gmail.com')
        self.assertEqual('Test Title', revision.title)
        self.assertEqual(100.1, revision.sequence)
        self.assertEqual('Eric Blair', revision.author_name)
        self.assertEqual('eb1984@gmail.com', revision.author_email)

    def test_init_sequence_is_non_convertible(self):
        with self.assertRaises(ValueError):
            Revision(title='Test Title',
                     sequence='BAD VALUE',
                     author_name='Eric Blair',
                     author_email='eb1984@gmail.com')


class TestSource(unittest.TestCase):

    def test_init_requirement_is_str(self):
        source = Source('required')
        self.assertEqual(Requirement.REQUIRED, source.requirement)

    def test_init_requirement_is_requirement(self):
        source = Source(Requirement.REQUESTED)
        self.assertEqual(Requirement.REQUESTED, source.requirement)


if __name__ == '__main__':
    unittest.main()
