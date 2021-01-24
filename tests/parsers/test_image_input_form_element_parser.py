import unittest

from html_form_parser.parsers.form_element_parser import ImageInputFormElementParser


class Test_ImageInputFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<input />"
    TESTVALUE = "<input type=\"image\" name=\"test\" />"

    def test_parse(self):

        obj = ImageInputFormElementParser()
        elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(2, len(elements))
    
    def test_default_name(self):

        obj = ImageInputFormElementParser()
        elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual("x", elements[0].name)
        self.assertEqual("y", elements[1].name)
    
    def test_default_value(self):

        obj = ImageInputFormElementParser()
        elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(obj.DEFAULT_VALUE, elements[0].value)
        self.assertEqual(obj.DEFAULT_VALUE, elements[1].value)
    
    def test_default_is_selected(self):

        obj = ImageInputFormElementParser()
        elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertFalse(elements[0].is_selected)
        self.assertFalse(elements[1].is_selected)

    def test_name(self):

        obj = ImageInputFormElementParser()
        elements = obj.parse(self.TESTVALUE)

        self.assertEqual("test.x", elements[0].name)
        self.assertEqual("test.y", elements[1].name)