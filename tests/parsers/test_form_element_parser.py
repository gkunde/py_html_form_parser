import unittest

from bs4 import BeautifulSoup
from html_form_parser.parsers.form_element_parser import FormElementParser


class Test_FormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TESTVALUE = "<input type=\"foo\" name=\"bar\" value=\"fizz\" />"

    def test_parse(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertIsInstance(form_elements, (list, ))


    def test_parse_with_bs4_object(self):

        bs4_parser = BeautifulSoup(self.TESTVALUE, "html5lib")

        obj = FormElementParser()
        form_elements = obj.parse(bs4_parser.body.next_element)

        self.assertEqual(1, len(form_elements))

        self.assertEqual("input", form_elements[0].primary_type)
        self.assertEqual("foo", form_elements[0].secondary_type)
        self.assertEqual("bar", form_elements[0].name)
        self.assertEqual("fizz", form_elements[0].value)
        self.assertTrue(form_elements[0].is_selected)
        self.assertIsNone(form_elements[0].binary_path)

    def test_primary_type(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual("input", form_elements[0].primary_type)

    def test_default_secondary_type(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertIsNone(form_elements[0].secondary_type)
    
    def test_default_name(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertIsNone(form_elements[0].name)
    
    def test_default_value(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj.DEFAULT_VALUE, form_elements[0].value)
    
    def test_default_is_selected(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertTrue(form_elements[0].is_selected)

    def test_secondary_type(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual("foo", form_elements[0].secondary_type)
    
    def test_name(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual("bar", form_elements[0].name)
    
    def test_value(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual("fizz", form_elements[0].value)
    
    def test_is_selected(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertTrue(form_elements[0].is_selected)
