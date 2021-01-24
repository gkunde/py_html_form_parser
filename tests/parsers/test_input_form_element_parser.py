import unittest

from bs4 import BeautifulSoup
from html_form_parser.parsers.form_element_parser import InputFormElementParser


class Test_InputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TESTVALUE = "<input type=\"foo\" name=\"bar\" value=\"fizz\" />"

    def test_default_secondary_type(self):

        obj = InputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj.DEFAULT_TYPE, form_elements[0].secondary_type)

    def test_default_value(self):

        obj = InputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj.DEFAULT_VALUE, form_elements[0].value)
