import unittest

from html_form_parser.parsers.form_element_parser import RangeInputFormElementParser


class Test_RangeInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TEST_VALUE = "<input type=\"foo\" name=\"magic\" value=\"100\" />"

    def test_default_value(self):

        obj = RangeInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual("50", form_elements[0].value)

    def test_value(self):

        obj = RangeInputFormElementParser()
        form_elements = obj.parse(self.TEST_VALUE)

        self.assertEqual("100", form_elements[0].value)

    def test_default_min_max(self):

        obj = RangeInputFormElementParser()
        form_elements = obj.parse("<input min=\"30\" max=\"40\" />")

        self.assertEqual("35", form_elements[0].value)

    def test_default_max(self):

        obj = RangeInputFormElementParser()
        form_elements = obj.parse("<input max=\"10\" />")

        self.assertEqual("5", form_elements[0].value)

    def test_default_min(self):

        obj = RangeInputFormElementParser()
        form_elements = obj.parse("<input min=\"90\" />")

        self.assertEqual("95", form_elements[0].value)

    def test_max_less_than_min(self):

        obj = RangeInputFormElementParser()
        form_elements = obj.parse("<input max=\"-50\" min=\"-40\" />")

        self.assertEqual("-40", form_elements[0].value)

    def test_suitable(self):

        obj = RangeInputFormElementParser()
        result = obj.suitable("input", "range")

        self.assertTrue(result)

    def test_suitable_false(self):

        obj = RangeInputFormElementParser()
        result = obj.suitable("example", None)

        self.assertFalse(result)

    def test_suitable_false_valid_tag(self):

        obj = RangeInputFormElementParser()
        result = obj.suitable("input", "example")

        self.assertFalse(result)

    def test_suitable_false_valid_type(self):

        obj = RangeInputFormElementParser()
        result = obj.suitable("example", "range")

        self.assertFalse(result)
