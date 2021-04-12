import unittest

from html_form_parser.parsers.form_element_parser import ButtonInputFormElementParser


class Test_ButtonInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TEST_VALUE = "<input type=\"foo\" name=\"magic\" value=\"100\" />"

    def test_default_value(self):

        obj = ButtonInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertIsNone(form_elements[0].value)

    def test_default_name(self):

        obj = ButtonInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj._default_name, form_elements[0].name)

    def test_default_is_submitable(self):

        obj = ButtonInputFormElementParser()
        form_element = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertFalse(form_element[0].is_submitable)

    def test_suitable_button(self):

        obj = ButtonInputFormElementParser()
        result = obj.suitable("input", "button")

        self.assertTrue(result)

    def test_suitable_reset(self):

        obj = ButtonInputFormElementParser()
        result = obj.suitable("input", "reset")

        self.assertTrue(result)

    def test_suitable_search(self):

        obj = ButtonInputFormElementParser()
        result = obj.suitable("input", "search")

        self.assertTrue(result)

    def test_suitable_invalid_type(self):

        obj = ButtonInputFormElementParser()
        result = obj.suitable("input", "example")

        self.assertFalse(result)

    def test_suitable_button_invalid_tag(self):

        obj = ButtonInputFormElementParser()
        result = obj.suitable("example", "button")

        self.assertFalse(result)

    def test_suitable_reset_invalid_tag(self):

        obj = ButtonInputFormElementParser()
        result = obj.suitable("example", "reset")

        self.assertFalse(result)

    def test_suitable_search_invalid_tag(self):

        obj = ButtonInputFormElementParser()
        result = obj.suitable("example", "search")

        self.assertFalse(result)

    def test_suitable_invalid(self):

        obj = ButtonInputFormElementParser()
        result = obj.suitable("example", "example")

        self.assertFalse(result)
