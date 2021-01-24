import unittest

from html_form_parser.parsers.form_element_parser import ResetInputFormElementParser


class Test_ResetInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"

    def test_default_type(self):

        obj = ResetInputFormElementParser()
        elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj.DEFAULT_TYPE, elements[0].secondary_type)
    
    def test_default_is_selected(self):

        obj = ResetInputFormElementParser()
        elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertFalse(elements[0].is_selected)