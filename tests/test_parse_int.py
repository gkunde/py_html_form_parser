from html_form_parser import form_field
import unittest


class Test_ParseInt(unittest.TestCase):

    def test_str_to_int(self):

        test_value = "456"
        expected_value = 456

        result_value = form_field.parse_int(test_value)

        self.assertEqual(expected_value, result_value)

    def test_str_to_int_default(self):

        test_value = ""

        result_value = form_field.parse_int(test_value)

        self.assertIsNone(result_value)

    def test_str_to_int_default_set(self):

        test_value = ""
        default_value = 456
        expected_value = 456

        result_value = form_field.parse_int(test_value, default_value)

        self.assertEqual(expected_value, result_value)

    def test_none_to_int(self):

        test_value = None

        result_value = form_field.parse_int(test_value)

        self.assertIsNone(result_value)

    def test_float_to_int(self):

        test_value = 123.45
        expected_value = 123

        result_value = form_field.parse_int(test_value)

        self.assertEqual(expected_value, result_value)
    
    def test_int_to_int(self):

        test_value = 456
        result_value = form_field.parse_int(test_value)

        self.assertEqual(test_value, result_value)
        self.assertIs(test_value, result_value)
