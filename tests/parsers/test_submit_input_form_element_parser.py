import unittest

from html_form_parser.parsers.form_element_parser import SubmitInputFormElementParser


class Test_SubmitInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TEST_VALUE = "<input type=\"foo\" name=\"magic\" value=\"100\" />"

    def test_default_type(self):

        obj = SubmitInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj.DEFAULT_TYPE, form_elements[0].secondary_type)

    def test_default_value(self):

        obj = SubmitInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj.DEFAULT_VALUE, form_elements[0].value)

    def test_default_name(self):

        obj = SubmitInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj.DEFAULT_NAME, form_elements[0].name)

    def test_default_is_selected(self):

        obj = SubmitInputFormElementParser()
        form_element = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertFalse(form_element[0].is_selected)
