import unittest

from bs4 import BeautifulSoup
from html_form_parser.form_field import FormField


class Test_FormFieldModel(unittest.TestCase):

    def test_init_default(self):
        """
        test default property values
        """

        field_name = ""

        obj = FormField(field_name)

        self.assertEqual(field_name, obj.name)
        self.assertEqual("", obj.value)
        self.assertEqual(True, obj.is_selected)
        self.assertIsNone(obj.binary_path)

    def test_init_name_exception(self):
        """
        test name required on init
        """

        self.assertRaises(ValueError, FormField)

    def test_init_values(self):
        """
        test setting properties with initializer
        """

        field_name = "fieldName"
        field_value = "test_value"
        field_is_selected = False
        field_binary_path = ""

        obj = FormField(field_name, field_value, field_is_selected, field_binary_path)

        self.assertEqual(field_name, obj.name)
        self.assertEqual(field_value, obj.value)
        self.assertEqual(field_is_selected, obj.is_selected)
        self.assertEqual(field_binary_path, obj.binary_path)

    def test_setters(self):
        """
        test setting properties directly
        """

        field_name = "fieldName"
        field_name_altered = "alteredFieldname"
        field_value = "test_value"
        field_is_selected = False
        field_binary_path = ""

        obj = FormField(field_name)
        obj.name = field_name_altered
        obj.value = field_value
        obj.is_selected = field_is_selected
        obj.binary_path = field_binary_path

        self.assertEqual(field_name_altered, obj.name)
        self.assertEqual(field_value, obj.value)
        self.assertEqual(field_is_selected, obj.is_selected)
        self.assertEqual(field_binary_path, obj.binary_path)

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

        self.assertEqual(1, len(form_field))
        self.assertEqual(attrs["name"], form_field[0].name)
        self.assertEqual(attrs["value"], form_field[0].value)

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

    def test_from_bs4_textarea_notext(self):
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

        self.assertEqual(1, len(form_field))
        self.assertEqual(attrs["name"], form_field[0].name)
        self.assertEqual("", form_field[0].value)

    def test_from_bs4_textarea(self):
        """
        Verify input tags with no type default to text.
        """

        tag_name = "textarea"

        attrs = {
            "name": "test1234",
            "value": "test4321",
        }

        field = "<%s %s>%s</%s>" % (tag_name,
                                    " ".join("%s=\"%s\"" % (key, val, )
                                             for key, val in attrs.items()),
                                    attrs["value"],
                                    tag_name)

        bs4parser = BeautifulSoup(field, "html5lib").find(tag_name)

        form_field = FormField.from_bs4(bs4parser)

        self.assertEqual(1, len(form_field))
        self.assertEqual(attrs["name"], form_field[0].name)
        self.assertEqual(attrs["value"], form_field[0].value)

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
        opt0 = "<%s %s />" % (option_tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                        for key, val in option_attrs0.items()))
        opt1 = "<%s %s />" % (option_tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                        for key, val in option_attrs1.items()))
        fieldc = "</%s>" % (tag_name)

        bs4parser = BeautifulSoup("%s%s%s%s" % (
            field, opt0, opt1, fieldc, ), "html5lib").find(tag_name)

        form_field = FormField.from_bs4(bs4parser)

        self.assertEqual(2, len(form_field))

        self.assertEqual(select_attrs["name"], form_field[0].name)
        self.assertEqual(select_attrs["name"], form_field[1].name)

        self.assertEqual(option_attrs0["value"], form_field[0].value)
        self.assertEqual(option_attrs1["value"], form_field[1].value)

        self.assertFalse(form_field[0].is_selected)
        self.assertTrue(form_field[1].is_selected)

        self.assertIsNone(form_field[0].binary_path)
        self.assertIsNone(form_field[1].binary_path)

    def test_from_dict(self):
        """
        Verify dictionary is captured to object
        """

        attrs = {
            "name": "test1234",
            "value": "1234TEST",
            "is_selected": False,
            "binary_path": None
        }

        form_field = FormField.from_dict(attrs)

        self.assertEqual(attrs["name"], form_field.name)
        self.assertEqual(attrs["value"], form_field.value)
        self.assertFalse(form_field.is_selected)
        self.assertIsNone(form_field.binary_path)

    def test_to_dict(self):
        """
        Verify dump to dictionary
        """

        attrs = {
            "name": "test1234",
            "value": "test4321",
        }

        form_field = FormField(attrs["name"], attrs["value"]).to_dict()

        self.assertIn("name", form_field)
        self.assertIn("value", form_field)
        self.assertIn("is_selected", form_field)
        self.assertIn("binary_path", form_field)

        self.assertEqual(attrs["name"], form_field["name"])
        self.assertEqual(attrs["value"], form_field["value"])
        self.assertTrue(form_field["is_selected"])
        self.assertIsNone(form_field["binary_path"])
