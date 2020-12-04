import unittest

from bs4 import BeautifulSoup
from html_form_parser.form_control import FormControl


class Test_FormControlModel(unittest.TestCase):

    def test_init_default(self):
        """
        test default property values
        """

        obj = FormControl()

        self.assertEqual(None, obj.name)
        self.assertEqual(FormControl.DEFAULT_INPUT_TYPE, obj._type)
        self.assertEqual(0, len(obj.values))

    def test_init_values(self):
        """
        test setting properties with initializer
        """

        field_name = "fieldName"
        field_values = [None, None, ]

        obj = FormControl(field_name, field_values)

        self.assertEqual(field_name, obj.name)
        self.assertEqual(FormControl.DEFAULT_INPUT_TYPE, obj._type)
        self.assertEqual(len(field_values), len(obj.values))

    def test_setters(self):
        """
        test setting properties directly
        """

        field_name = "fieldName"
        field_type = "checkbox"
        field_values = [None, None, ]

        obj = FormControl()
        obj.name = field_name
        obj._type = field_type
        obj.values_add_range(field_values)

        self.assertEqual(field_name, obj.name)
        self.assertEqual(field_type, obj._type)
        self.assertEqual(len(field_values), len(obj.values))

    def test_value_append(self):
        """
        test appending values to the field
        """

        obj = FormControl()
        obj.values_append(None)

        self.assertEqual(1, len(obj.values))

    def test_from_bs4(self):
        """
        Generic BeautifulSoup object parse
        """

        tag_name = "input"

        attrs = {
            "type": "submit",
            "name": "test1234",
            "value": "test4321",
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        bs4parser = BeautifulSoup(field, "html5lib").find(tag_name)

        form_field = FormControl.from_bs4(bs4parser)

        self.assertEqual(attrs["type"], form_field._type)
        self.assertEqual(attrs["name"], form_field.name)
        self.assertEqual(1, len(form_field.values))

    def test_from_bs4_invalid_tag(self):
        """
        Non-form field tag raises error
        """

        tag_name = "p"

        attrs = {
            "type": "text",
            "name": "test1234",
            "value": "test4321",
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        bs4parser = BeautifulSoup(field, "html5lib").find(tag_name)

        self.assertRaises(ValueError, FormControl.from_bs4, bs4parser)

    def test_from_bs4_invalid_input_type(self):
        """
        A control field type raises errors
        """

        tag_name = "input"

        attrs = {
            "type": "text",
            "name": "test1234",
            "value": "test4321",
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        bs4parser = BeautifulSoup(field, "html5lib").find(tag_name)

        self.assertRaises(ValueError, FormControl.from_bs4, bs4parser)

    def test_from_bs4_input_default_type(self):
        """
        Verify input tags with no type default to text.
        """

        tag_name = "input"

        attrs = {
            "name": "test1234",
            "value": "test4321",
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        bs4parser = BeautifulSoup(field, "html5lib").find(tag_name)

        form_field = FormControl.from_bs4(bs4parser)

        self.assertEqual(FormControl.DEFAULT_INPUT_TYPE, form_field._type)
        self.assertEqual(attrs["name"], form_field.name)
        self.assertEqual(1, len(form_field.values))

    def test_from_dict(self):
        """
        Verify dictionary is captured to object
        """

        attrs = {
            "name": "test1234",
            "values": [],
        }

        form_field = FormControl.from_dict(attrs)

        self.assertEqual(attrs["name"], form_field.name)
        self.assertEqual(FormControl.DEFAULT_INPUT_TYPE, form_field._type)
        self.assertEqual(0, len(form_field.values))

    def test_from_dict_with_values(self):
        """
        Verify values are captured.
        """

        attrs = {
            "name": "test1234",
            "values": [{"value": "test4321", "is_selected": True}]
        }

        form_field = FormControl.from_dict(attrs)

        self.assertEqual(attrs["name"], form_field.name)
        self.assertEqual(FormControl.DEFAULT_INPUT_TYPE, form_field._type)
        self.assertEqual(1, len(form_field.values))

    def test_to_dict(self):
        """
        Verify dump to dictionary
        """

        attrs = {
            "name": "test1234",
            "values": [{"value": "test4321", "is_selected": True, "binary_path": None}]
        }

        form_field = FormControl.from_dict(attrs).to_dict()

        self.assertEqual(attrs["name"], form_field["name"])
        self.assertEqual(attrs["values"], form_field["values"])
