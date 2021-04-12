import unittest

from bs4 import BeautifulSoup
from html_form_parser.parsers.form_element_parser import InputFormElementParser


class Test_InputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TESTVALUE = "<input type=\"foo\" name=\"bar\" value=\"fizz\" />"

    def test_default_value(self):

        obj = InputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj._default_value, form_elements[0].value)

    def test_suitable(self):

        obj = InputFormElementParser()
        result = obj.suitable("input", None)

        self.assertTrue(result)

    def test_suitable_false(self):

        obj = InputFormElementParser()
        result = obj.suitable("example", None)

        self.assertFalse(result)

    def test_suitable_true_valid_tag(self):

        obj = InputFormElementParser()
        result = obj.suitable("input", "example")

        self.assertTrue(result)
