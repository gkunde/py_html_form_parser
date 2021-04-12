import unittest

from html_form_parser.parsers.form_element_parser import SelectableInputFormElementParser


class Test_CheckboxInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TESTVALUE = "<input type=\"checkbox\" name=\"test1234\" value=\"123456\" checked />"

    def test_default_value(self):

        obj = SelectableInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj._default_value, form_elements[0].value)

    def test_default_is_submitable(self):

        obj = SelectableInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertFalse(form_elements[0].is_submitable)

    def test_is_submitable(self):

        obj = SelectableInputFormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertTrue(form_elements[0].is_submitable)

    def test_suitable_checkbox(self):

        obj = SelectableInputFormElementParser()
        result = obj.suitable("input", "checkbox")

        self.assertTrue(result)

    def test_suitable_radio(self):

        obj = SelectableInputFormElementParser()
        result = obj.suitable("input", "radio")

        self.assertTrue(result)

    def test_suitable_invalid_type(self):

        obj = SelectableInputFormElementParser()
        result = obj.suitable("input", "example")

        self.assertFalse(result)

    def test_suitable_checkbox_invalid_tag(self):

        obj = SelectableInputFormElementParser()
        result = obj.suitable("example", "checkbox")

        self.assertFalse(result)

    def test_suitable_radio_invalid_tag(self):

        obj = SelectableInputFormElementParser()
        result = obj.suitable("example", "radio")

        self.assertFalse(result)

    def test_suitable_invalid(self):

        obj = SelectableInputFormElementParser()
        result = obj.suitable("example", "example")

        self.assertFalse(result)
