import unittest

from html_form_parser.parsers.form_element_parser import RadioInputFormElementParser


class Test_RadioInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TESTVALUE = "<input type=\"radio\" name=\"test1234\" value=\"123456\" checked />"

    def test_default_secondary_type(self):

        obj = RadioInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj.DEFAULT_TYPE, form_elements[0].secondary_type)

    def test_default_value(self):

        obj = RadioInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj.DEFAULT_VALUE, form_elements[0].value)

    def test_default_is_selected(self):

        obj = RadioInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertFalse(form_elements[0].is_selected)

    def test_is_selected(self):

        obj = RadioInputFormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertTrue(form_elements[0].is_selected)
