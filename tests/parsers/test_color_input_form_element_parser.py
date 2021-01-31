import unittest

from html_form_parser.parsers.form_element_parser import ColorInputFormElementParser


class Test_ColorInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TESTVALUE = "<input type=\"color\" name=\"test1234\" value=\"#123456\" />"

    def test_default_secondary_type(self):

        obj = ColorInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj._default_type, form_elements[0].type_attribute)

    def test_default_value(self):

        obj = ColorInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj._default_value, form_elements[0].value)

    def test_value(self):

        obj = ColorInputFormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual("#123456", form_elements[0].value)
