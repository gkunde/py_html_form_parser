import unittest

from html_form_parser.parsers.form_element_parser import SubmitInputFormElementParser


class Test_SubmitInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TEST_VALUE = "<input type=\"foo\" name=\"magic\" value=\"100\" />"

    def test_default_type(self):

        obj = SubmitInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj._default_type, form_elements[0].type_attribute)

    def test_default_value(self):

        obj = SubmitInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj._default_value, form_elements[0].value)

    def test_default_name(self):

        obj = SubmitInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj._default_name, form_elements[0].name)

    def test_default_is_selected(self):

        obj = SubmitInputFormElementParser()
        form_element = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertFalse(form_element[0].is_selected)

    def test_suitable(self):

        obj = SubmitInputFormElementParser()
        result = obj.suitable("input", "submit")

        self.assertTrue(result)
    
    def test_suitable_false(self):

        obj = SubmitInputFormElementParser()
        result = obj.suitable("example", "example")

        self.assertFalse(result)

    def test_suitable_false_valid_tag(self):

        obj = SubmitInputFormElementParser()
        result = obj.suitable("input", "example")

        self.assertFalse(result)
    
    def test_suitable_false_valid_type(self):

        obj = SubmitInputFormElementParser()
        result = obj.suitable("example", "submit")

        self.assertFalse(result)