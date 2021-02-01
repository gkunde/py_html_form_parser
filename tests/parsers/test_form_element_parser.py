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

        self.assertEqual("input", form_elements[0].tag_name)
        self.assertEqual("foo", form_elements[0].type_attribute)
        self.assertEqual("bar", form_elements[0].name)
        self.assertEqual("fizz", form_elements[0].value)
        self.assertTrue(form_elements[0].is_selected)
        self.assertIsNone(form_elements[0].binary_path)

    def test_primary_type(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual("input", form_elements[0].tag_name)

    def test_default_secondary_type(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertIsNone(form_elements[0].type_attribute)
    
    def test_default_name(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertIsNone(form_elements[0].name)
    
    def test_default_value(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual(obj._default_value, form_elements[0].value)
    
    def test_default_is_selected(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertTrue(form_elements[0].is_selected)

    def test_secondary_type(self):

        obj = FormElementParser()
        form_elements = obj.parse(self.TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertEqual("foo", form_elements[0].type_attribute)
    
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
    
    def test_suitable(self):

        obj = FormElementParser()
        result = obj.suitable("input", "example")

        self.assertTrue(result)
    
    def test_suitable_false_invalid_tag(self):

        obj = FormElementParser()
        result = obj.suitable("example", "example")

        self.assertFalse(result)
