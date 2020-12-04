import unittest

from bs4 import BeautifulSoup
from html_form_parser.form_field import FormField
from html_form_parser.form_field_value import FormFieldValue


class Test_FormFieldModel(unittest.TestCase):

    def test_init_default(self):
        """
        test default property values
        """

        obj = FormField()

        self.assertEqual(None, obj.name)
        self.assertEqual(FormField.DEFAULT_INPUT_TYPE, obj._type)
        self.assertEqual(0, len(obj.values))

    def test_init_values(self):
        """
        test setting properties with initializer
        """

        field_name = "fieldName"
        field_values = [None, None, ]

        obj = FormField(field_name, field_values)

        self.assertEqual(field_name, obj.name)
        self.assertEqual(FormField.DEFAULT_INPUT_TYPE, obj._type)
        self.assertEqual(len(field_values), len(obj.values))

    def test_setters(self):
        """
        test setting properties directly
        """

        field_name = "fieldName"
        field_type = "checkbox"
        field_values = [FormFieldValue("test1234"), FormFieldValue("test1235"), ]

        obj = FormField()
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

        obj = FormField()
        obj.values_append(FormFieldValue("test1234"))

        self.assertEqual(1, len(obj.values))

    def test_from_bs4(self):
        """
        Generic BeautifulSoup object parse
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

        form_field = FormField.from_bs4(bs4parser)

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

        self.assertRaises(ValueError, FormField.from_bs4, bs4parser)

    def test_from_bs4_invalid_input_type(self):
        """
        A control field type raises errors
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

        self.assertRaises(ValueError, FormField.from_bs4, bs4parser)

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

        form_field = FormField.from_bs4(bs4parser)

        self.assertEqual(FormField.DEFAULT_INPUT_TYPE, form_field._type)
        self.assertEqual(attrs["name"], form_field.name)
        self.assertEqual(1, len(form_field.values))

    def test_from_bs4_textarea_default_type(self):
        """
        Verify input tags with no type default to text.
        """

        tag_name = "textarea"

        attrs = {
            "name": "test1234",
            "value": "test4321",
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        bs4parser = BeautifulSoup(field, "html5lib").find(tag_name)

        form_field = FormField.from_bs4(bs4parser)

        self.assertEqual("", form_field._type)
        self.assertEqual(attrs["name"], form_field.name)
        self.assertEqual(1, len(form_field.values))

    def test_from_bs4_select(self):
        """
        Verify that <select /> is parsed and all options captured as values.
        """

        tag_name = "select"

        select_attrs = {
            "name": "test1234"
        }

        option_tag_name = "option"
        option_attrs0 = {
            "value": "test4321"
        }

        option_attrs1 = {
            "value": "test4322",
            "selected": None
        }

        field = "<%s %s>" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                for key, val in select_attrs.items()))
        opt0 = "<%s %s>" % (option_tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                      for key, val in option_attrs0.items()))
        opt1 = "<%s %s>" % (option_tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                      for key, val in option_attrs1.items()))
        fieldc = "</%s>" % (tag_name)

        bs4parser = BeautifulSoup("%s%s%s%s" % (
            field, opt0, opt1, fieldc, ), "html5lib").find(tag_name)

        form_field = FormField.from_bs4(bs4parser)

        self.assertEqual(select_attrs["name"], form_field.name)

        self.assertEqual(2, len(form_field.values))

        self.assertEqual(option_attrs0["value"], form_field.values[0].value)
        self.assertFalse(form_field.values[0].is_selected)

        self.assertEqual(option_attrs1["value"], form_field.values[1].value)
        self.assertTrue(form_field.values[1].is_selected)

    def test_from_dict(self):
        """
        Verify dictionary is captured to object
        """

        attrs = {
            "name": "test1234",
            "values": [],
        }

        form_field = FormField.from_dict(attrs)

        self.assertEqual(attrs["name"], form_field.name)
        self.assertEqual(FormField.DEFAULT_INPUT_TYPE, form_field._type)
        self.assertEqual(0, len(form_field.values))

    def test_from_dict_with_values(self):
        """
        Verify values are captured.
        """

        attrs = {
            "name": "test1234",
            "values": [{"value": "test4321", "is_selected": True}]
        }

        form_field = FormField.from_dict(attrs)

        self.assertEqual(attrs["name"], form_field.name)
        self.assertEqual(FormField.DEFAULT_INPUT_TYPE, form_field._type)
        self.assertEqual(1, len(form_field.values))

    def test_to_dict(self):
        """
        Verify dump to dictionary
        """

        attrs = {
            "name": "test1234",
            "values": [{"value": "test4321", "is_selected": True, "binary_path": None}]
        }

        form_field = FormField.from_dict(attrs).to_dict()

        self.assertEqual(attrs["name"], form_field["name"])
        self.assertEqual(attrs["values"], form_field["values"])
