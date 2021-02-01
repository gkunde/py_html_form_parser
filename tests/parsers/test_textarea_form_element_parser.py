import unittest

from html_form_parser.parsers.form_element_parser import TextareaFormElementParser


class Test_TextareaFormelementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<textarea></textarea>"

    def test_default_secondary_type(self):

        obj = TextareaFormElementParser()
        form_elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(1, len(form_elements))
        self.assertIsNone(form_elements[0].type_attribute)

    def test_parse_value(self):

        obj = TextareaFormElementParser()
        form_elements = obj.parse("<textarea>Some text to find.</textarea>")

        self.assertEqual(1, len(form_elements))
        self.assertEqual("Some text to find.", form_elements[0].value)
    
    def test_parse_malformed_tag(self):

        obj = TextareaFormElementParser()
        form_elements = obj.parse("<textarea />")

        self.assertEqual(1, len(form_elements))
        self.assertEqual("", form_elements[0].value)

    def test_suitable(self):

        obj = TextareaFormElementParser()
        result = obj.suitable("textarea", None)

        self.assertTrue(result)

    def test_suitable_false(self):

        obj = TextareaFormElementParser()
        result = obj.suitable("input", None)

        self.assertFalse(result)

    def test_suitable_true_w_type(self):

        obj = TextareaFormElementParser()
        result = obj.suitable("textarea", "random")

        self.assertTrue(result)

    def test_suitable_false_w_type(self):

        obj = TextareaFormElementParser()
        result = obj.suitable("foo", "random")

        self.assertFalse(result)
