import unittest

from bs4 import BeautifulSoup
from html_form_parser.parsers.form_element_parser import ButtonFormElementParser


class Test_ButtonFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<button />"
    TESTVALUE = "<button type=\"foo\" name=\"bar\" value=\"fizz\" />"

    def test_default_secondary_type(self):

        obj = ButtonFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj.DEFAULT_TYPE, form_elements[0].secondary_type)

    def test_default_value(self):

        obj = ButtonFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj.DEFAULT_VALUE, form_elements[0].value)

    def test_default_is_selected(self):

        obj = ButtonFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertFalse(form_elements[0].is_selected)

    def test_secondary_type(self):

        obj = ButtonFormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual("foo", form_elements[0].secondary_type)

    def test_is_selected(self):

        obj = ButtonFormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertFalse(form_elements[0].is_selected)
