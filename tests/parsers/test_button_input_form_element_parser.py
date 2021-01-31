import unittest

from html_form_parser.parsers.form_element_parser import ButtonInputFormElementParser


class Test_ButtonInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TEST_VALUE = "<input type=\"foo\" name=\"magic\" value=\"100\" />"

    def test_default_type(self):

        obj = ButtonInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj._default_type, form_elements[0].type_attribute)

    def test_default_value(self):

        obj = ButtonInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertIsNone(form_elements[0].value)

    def test_default_name(self):

        obj = ButtonInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj._default_name, form_elements[0].name)

    def test_default_is_selected(self):

        obj = ButtonInputFormElementParser()
        form_element = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertFalse(form_element[0].is_selected)
