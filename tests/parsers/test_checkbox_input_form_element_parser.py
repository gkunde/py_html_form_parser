import unittest

from html_form_parser.parsers.form_element_parser import CheckboxInputFormElementParser


class Test_CheckboxInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TESTVALUE = "<input type=\"checkbox\" name=\"test1234\" value=\"123456\" checked />"

    def test_default_secondary_type(self):

        obj = CheckboxInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj.DEFAULT_TYPE, form_elements[0].secondary_type)

    def test_default_value(self):

        obj = CheckboxInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj.DEFAULT_VALUE, form_elements[0].value)

    def test_default_is_selected(self):

        obj = CheckboxInputFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertFalse(form_elements[0].is_selected)

    def test_is_selected(self):

        obj = CheckboxInputFormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertTrue(form_elements[0].is_selected)
