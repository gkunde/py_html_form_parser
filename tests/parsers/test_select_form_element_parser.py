import unittest

from html_form_parser.parsers.form_element_parser import SelectFormElementParser


class Test_SelectFormElementParser(unittest.TestCase):

    DEFAULT_TESTVALUE = "<select />"

    TESTVALUE = "<select name=\"foo\"><option value=\"fizz\" /><option value=\"buzz\" /><option value=\"woof\" /></select>"
    TESTVALUE_NONAME = "<select><option value=\"fizz\" /><option value=\"buzz\" /><option value=\"woof\" /></select>"
    TESTVALUE_CLASSICVALUE = "<select><option selected>fizz</option><option>buzz</option><option>woof</option></select>"

    def test_parse_default(self):

        obj = SelectFormElementParser()
        elements = obj.parse(self.DEFAULT_TESTVALUE)

        self.assertEqual(0, len(elements))

    def test_parse(self):

        obj = SelectFormElementParser()
        elements = obj.parse(self.TESTVALUE)

        self.assertEqual(3, len(elements))

    def test_default_name(self):

        obj = SelectFormElementParser()
        elements = obj.parse(self.TESTVALUE_NONAME)

        self.assertIsNone(elements[0].name)

    def test_name(self):

        obj = SelectFormElementParser()
        elements = obj.parse(self.TESTVALUE)

        self.assertEqual("foo", elements[0].name)
        self.assertEqual("foo", elements[1].name)
        self.assertEqual("foo", elements[2].name)

    def test_inline_value(self):

        obj = SelectFormElementParser()
        elements = obj.parse(self.TESTVALUE_CLASSICVALUE)

        self.assertEqual("fizz", elements[0].value)
        self.assertEqual("buzz", elements[1].value)
        self.assertEqual("woof", elements[2].value)

    def test_attr_value(self):

        obj = SelectFormElementParser()
        elements = obj.parse(self.TESTVALUE_NONAME)

        self.assertEqual("fizz", elements[0].value)
        self.assertEqual("buzz", elements[1].value)
        self.assertEqual("woof", elements[2].value)

    def test_is_selected(self):

        obj = SelectFormElementParser()
        elements = obj.parse(self.TESTVALUE_CLASSICVALUE)

        self.assertTrue(elements[0].is_selected)
        self.assertFalse(elements[1].is_selected)
        self.assertFalse(elements[2].is_selected)

    def test_suitable(self):

        obj = SelectFormElementParser()
        result = obj.suitable("select", None)

        self.assertTrue(result)

    def test_suitable_false(self):

        obj = SelectFormElementParser()
        result = obj.suitable("example", None)

        self.assertFalse(result)

    def test_suitable_true_valid_tag(self):

        obj = SelectFormElementParser()
        result = obj.suitable("select", "example")

        self.assertTrue(result)
