import unittest
from bs4 import BeautifulSoup

from html_form_parser import form_field_value


class Test_parse_int(unittest.TestCase):
    """
    Test the parse_int helper function
    """

    def test_str(self):
        """
        Test a string representation of integer is returned
        """

        test_value = "50"
        expected = 50

        result = form_field_value.parse_int(test_value, 0)

        self.assertEqual(expected, result)

    def test_str_bad_value(self):
        """
        Test a string with invalid value.
        """

        test_value = "ONE"
        expected = 1

        result = form_field_value.parse_int(test_value, 1)

        self.assertEqual(expected, result)

    def test_int(self):
        """
        Test that a provided int value is directly returned.
        """

        test_value = 67

        result = form_field_value.parse_int(test_value, 0)

        self.assertEqual(test_value, result)

    def test_bool(self):
        """
        Test that a provided int value is directly returned.
        """

        test_value = True
        expected = int(True)

        result = form_field_value.parse_int(test_value, 0)

        self.assertEqual(expected, result)

    def test_float(self):
        """
        Test that a float is returned as its whole value
        """

        test_value = 50.0
        expected = int(test_value)

        result = form_field_value.parse_int(test_value, 0)

        self.assertEqual(expected, result)


class Test_FormFieldValue(unittest.TestCase):

    def test_init_default(self):
        """
        Test default initialization of object.
        """

        obj = form_field_value.FormFieldValue()

        self.assertEqual(None, obj.value)
        self.assertEqual(True, obj.is_selected)
        self.assertEqual(None, obj.binary_path)

    def test_init_values(self):
        """
        Test properties set by initialize
        """

        field_value = "test1234"
        field_selected = False
        field_binary_path = "test4321"

        obj = form_field_value.FormFieldValue(field_value, field_selected, field_binary_path)

        self.assertEqual(field_value, obj.value)
        self.assertEqual(field_selected, obj.is_selected)
        self.assertEqual(field_binary_path, obj.binary_path)

    def test_setters(self):
        """
        Test properties set by setters
        """

        field_value = "test1234"
        field_selected = False
        field_binary_path = "test4321"

        obj = form_field_value.FormFieldValue()
        obj.value = field_value
        obj.is_selected = field_selected
        obj.binary_path = field_binary_path

        self.assertEqual(field_value, obj.value)
        self.assertEqual(field_selected, obj.is_selected)
        self.assertEqual(field_binary_path, obj.binary_path)

    def test_from_bs4_text(self):
        """
        Test that a general text field is parsed.
        """

        attrs = {
            "type": "text",
            "name": "test1234",
            "value": "test4321"
        }

        field = "<input %s />" % (" ".join("%s=\"%s\"" % (key, val, )
                                           for key, val in attrs.items()))

        bs4parser = BeautifulSoup(field, "html5lib").find("input")

        formfieldvalue = form_field_value.FormFieldValue.from_bs4(bs4parser)

        self.assertEqual(attrs["value"], formfieldvalue.value)
        self.assertEqual(None, formfieldvalue.binary_path)
        self.assertTrue(formfieldvalue.is_selected)

    def test_from_bs4_checkbox(self):
        """
        Test that a range field is parsed and a default value is returned.
        """

        attrs = {
            "type": "checkbox",
            "name": "test1234",
        }

        field = "<input %s />" % (" ".join("%s=\"%s\"" % (key, val, )
                                           for key, val in attrs.items()))

        bs4parser = BeautifulSoup(field, "html5lib").find("input")

        formfieldvalue = form_field_value.FormFieldValue.from_bs4(bs4parser)

        self.assertEqual("on", formfieldvalue.value)
        self.assertEqual(None, formfieldvalue.binary_path)
        self.assertFalse(formfieldvalue.is_selected)

    def test_from_dict(self):
        """
        Test dictionary parsing
        """

        attrs = {
            "type": "text",
            "name": "test1234",
            "value": "test4321",
            "is_selected": False
        }

        formfieldvalue = form_field_value.FormFieldValue.from_dict(attrs)

        self.assertEqual(attrs["value"], formfieldvalue.value)
        self.assertEqual(None, formfieldvalue.binary_path)
        self.assertEqual(attrs["is_selected"], formfieldvalue.is_selected)

    def test_to_dict(self):
        """
        Test dictionary parsing
        """

        attrs = {
            "type": "text",
            "name": "test1234",
            "value": "test4321",
            "is_selected": False
        }

        formfieldvalue = form_field_value.FormFieldValue.from_dict(attrs).to_dict()

        self.assertEqual(attrs["value"], formfieldvalue["value"])
        self.assertEqual(None, formfieldvalue["binary_path"])
        self.assertEqual(attrs["is_selected"], formfieldvalue["is_selected"])

    def test_parse_input_value_text(self):
        """
        Test the value parser for returning a default value for text inputs.
        """

        result = form_field_value.FormFieldValue.parse_input_value("input", None, {})

        self.assertEqual("", result)

    def test_parse_input_value_range_default(self):
        """
        Test the input field range type value parser with no value.
        """

        attrs = {
            "type": "range",
            "name": "test1234",
        }

        result = form_field_value.FormFieldValue.parse_input_value("input", None, attrs)

        self.assertEqual("50", result)

    def test_parse_input_value_range_parsed(self):
        """
        Test the input field range type value parser
        """

        attrs = {
            "type": "range",
            "name": "test1234",
            "value": "176"
        }

        result = form_field_value.FormFieldValue.parse_input_value("input", None, attrs)

        self.assertEqual(attrs["value"], result)

    def test_parse_input_value_range_default_min_max(self):
        """
        Test the input field range type value parser default value when
        provided min and max attributes.
        """

        attrs = {
            "type": "range",
            "name": "test1234",
            "min": "10",
            "max": "30",
        }

        result = form_field_value.FormFieldValue.parse_input_value("input", None, attrs)

        self.assertEqual("20", result)

    def test_parse_input_value_range_default_max_too_small(self):
        """
        Test the input field range type value parser default value when
        provided min and max attributes, where max is smaller than min.
        """

        attrs = {
            "type": "range",
            "name": "test1234",
            "min": "10",
            "max": "5",
        }

        result = form_field_value.FormFieldValue.parse_input_value("input", None, attrs)

        self.assertEqual(attrs["min"], result)

    def test_parse_input_value_button(self):
        """
        Test that the inline text of the field is returned as a value.
        """

        attrs = {
            "type": "submit",
            "name": "submit"
        }

        tag_text = "Process"

        for tag_name in ("button", "option", "textarea", ):

            result = form_field_value.FormFieldValue.parse_input_value(tag_name, tag_text, attrs)

            self.assertEqual(tag_text, result)

    def test_parse_input_value_input_checkbox(self):
        """
        Test the checkbox and radio buttons provide default value.
        """

        attrs = {
            "type": "checkbox",
            "name": "test1234"
        }

        result = form_field_value.FormFieldValue.parse_input_value("input", None, attrs)
        self.assertEqual("on", result)

    def test_parse_input_value_input_radio(self):
        """
        Test the checkbox and radio buttons provide default value.
        """

        attrs = {
            "type": "radio",
            "name": "test1234"
        }

        result = form_field_value.FormFieldValue.parse_input_value("input", None, attrs)
        self.assertEqual("on", result)

    def test_parse_input_value_color_default(self):
        """
        Test the color input returns default value
        """

        attrs = {
            "type": "color",
            "name": "test1234"
        }

        result = form_field_value.FormFieldValue.parse_input_value("input", None, attrs)
        self.assertEqual("#000000", result)

    def test_parse_input_value_input_submit(self):
        """
        Test that a default value is returned for input submit types
        """

        attrs = {
            "type": "submit",
            "name": "test1234"
        }

        result = form_field_value.FormFieldValue.parse_input_value("input", None, attrs)

        self.assertEqual("Submit Query", result)

    def test_parse_selected_status_default(self):
        """
        Verify selected status for input is true
        """

        tag_name = "input"
        attrs = {
            "type": "text",
            "name": "test1234"
        }

        result = form_field_value.FormFieldValue.parse_selected_status(tag_name, attrs)

        self.assertTrue(result)

    def test_parse_selected_status_button(self):
        """
        Verify buttons are always is_selected = False
        """

        tag_name = "button"
        attrs = {
            "type": "submit",
            "name": "test1234"
        }

        result = form_field_value.FormFieldValue.parse_selected_status(tag_name, attrs)

        self.assertFalse(result)

    def test_parse_selected_status_input_submit(self):
        """
        Verify buttons are always is_selected = False
        """

        tag_name = "input"
        attrs = {
            "type": "submit",
            "name": "test1234"
        }

        result = form_field_value.FormFieldValue.parse_selected_status(tag_name, attrs)

        self.assertFalse(result)

    def test_parse_selected_status_option(self):
        """
        Verify select option is parsed false when not selected.
        """

        tag_name = "option"
        attrs = {
            "value": "test4321"
        }

        result = form_field_value.FormFieldValue.parse_selected_status(tag_name, attrs)

        self.assertFalse(result)

    def test_parse_selected_status_option_selected(self):
        """
        Verify select option is parsed true when selected.
        """

        tag_name = "option"
        attrs = {
            "value": "test4321",
            "selected": None
        }

        result = form_field_value.FormFieldValue.parse_selected_status(tag_name, attrs)

        self.assertTrue(result)

    def test_parse_selected_status_checkbox(self):
        """
        Verify checkbox is not selected when not checked
        """

        tag_name = "input"
        attrs = {
            "type": "checkbox",
            "value": "test4321"
        }

        result = form_field_value.FormFieldValue.parse_selected_status(tag_name, attrs)

        self.assertFalse(result)

    def test_parse_selected_status_checkbox_checked(self):
        """
        Verify checkbox is selected when checked.
        """

        tag_name = "input"
        attrs = {
            "type": "checkbox",
            "value": "test4321",
            "checked": None
        }

        result = form_field_value.FormFieldValue.parse_selected_status(tag_name, attrs)

        self.assertTrue(result)

    def test_parse_selected_status_radio(self):
        """
        Verify radio is not selected when not checked
        """

        tag_name = "input"
        attrs = {
            "type": "radio",
            "value": "test4321"
        }

        result = form_field_value.FormFieldValue.parse_selected_status(tag_name, attrs)

        self.assertFalse(result)

    def test_parse_selected_status_radio_checked(self):
        """
        Verify radio is selected when checked.
        """

        tag_name = "input"
        attrs = {
            "type": "radio",
            "value": "test4321",
            "checked": None
        }

        result = form_field_value.FormFieldValue.parse_selected_status(tag_name, attrs)

        self.assertTrue(result)
