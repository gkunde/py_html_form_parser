import unittest
from bs4 import BeautifulSoup

from html_form_parser.form import Form
from html_form_parser.form_control import FormControl
from html_form_parser.form_field import FormField
from html_form_parser.form_field_value import FormFieldValue


class Test_FormModel(unittest.TestCase):

    def test_init_default(self):
        """
        test default values when instantiating object with no values.
        """

        obj = Form()

        self.assertEqual(None, obj.name)
        self.assertEqual(None, obj.id)
        self.assertEqual(Form.DEFAULT_CHARSET, obj.accepted_charset)
        self.assertEqual(Form.DEFAULT_ENCODING_TYPE, obj.encoding_type)
        self.assertEqual(Form.DEFAULT_METHOD, obj.method)
        self.assertEqual(0, len(obj.fields))

    def test_init_values(self):
        """
        test property values set by initializer
        """

        form_name = "form1"
        form_id = "id1"
        form_fields = [FormField("test1234"), FormField("test1235"), ]

        obj = Form(form_name, form_id, form_fields)

        self.assertEqual(form_name, obj.name)
        self.assertEqual(form_id, obj.id)
        self.assertEqual(Form.DEFAULT_CHARSET, obj.accepted_charset)
        self.assertEqual(Form.DEFAULT_ENCODING_TYPE, obj.encoding_type)
        self.assertEqual(Form.DEFAULT_METHOD, obj.method)
        self.assertEqual(len(form_fields), len(obj.fields))

    def test_setters(self):
        """
        test setting properties via model setters
        """

        form_name = "form1"
        form_id = "id1"
        form_fields = [FormField("test1234"), FormField("test1235"), ]
        form_accepted_char_set = "8859-1"
        form_method = "POST"
        form_encoding_type = "text/plain"

        obj = Form()
        obj.name = form_name
        obj.id = form_id
        obj.accepted_charset = form_accepted_char_set
        obj.encoding_type = form_encoding_type
        obj.method = form_method
        obj.fields_add_range(form_fields)

        self.assertEqual(form_name, obj.name)
        self.assertEqual(form_id, obj.id)
        self.assertEqual(form_accepted_char_set, obj.accepted_charset)
        self.assertEqual(form_encoding_type, obj.encoding_type)
        self.assertEqual(form_method, obj.method)
        self.assertEqual(2, len(obj.fields))

    def test_append_field(self):
        """
        test appending form fields to form
        """

        obj = Form()
        obj.fields_append(FormField("test1234"))

        self.assertEqual(1, len(obj.fields))

    def test_fields_add_range(self):
        """
        test appending form fields to form
        """

        obj = Form()
        obj.fields_add_range([FormField("test1234"), ])

        self.assertEqual(1, len(obj.fields))

    def test_fields_add_range_multivalue(self):
        """
        Verify multiple fields with the same type and name have values merged.
        """

        obj = Form()
        obj.fields_add_range([FormField("test1234", [FormFieldValue("test4321")]),
                              FormField("test1234", [FormFieldValue("test4322")])])

        self.assertEqual(1, len(obj.fields))
        self.assertEqual(2, len(obj.fields[0].values))

    def test_controls_append(self):
        """
        test appending form fields to form
        """

        obj = Form()
        obj.controls_append(FormControl("test1234"))

        self.assertEqual(1, len(obj.controls))

    def test_controls_add_range(self):
        """
        test appending form fields to form
        """

        obj = Form()
        obj.controls_add_range([FormControl("test1234"), ])

        self.assertEqual(1, len(obj.controls))

    def test_controls_add_range_multivalue(self):
        """
        Verify multiple fields with the same type and name have values merged.
        """

        obj = Form()
        obj.controls_add_range([FormControl("test1234", [FormFieldValue("test4321")]),
                                FormControl("test1234", [FormFieldValue("test4322")])])

        self.assertEqual(1, len(obj.controls))
        self.assertEqual(2, len(obj.controls[0].values))

    def test_from_bs4(self):
        """
        Test parsing basic form.
        """

        form_tag = "form"
        form_attrs = {"name": "test1234"}
        form_element = "<%s %s>" % (form_tag, " ".join("%s=\"%s\"" % (key, val)
                                                       for key, val in form_attrs.items()))

        form_element_c = "</%s>" % (form_tag)

        tag_name = "input"

        attrs = {
            "name": "test1234",
            "value": "test4321",
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        html = "".join([form_element, field, form_element_c, ])

        bs4parser = BeautifulSoup(html, "html5lib").find(form_tag)

        form = Form.from_bs4(bs4parser)

        self.assertEqual(form_attrs["name"], form.name)
        self.assertEqual(Form.DEFAULT_ENCODING_TYPE, form.encoding_type)
        self.assertEqual(Form.DEFAULT_METHOD, form.method)
        self.assertEqual(Form.DEFAULT_CHARSET, form.accepted_charset)
        self.assertEqual(1, len(form.fields))
        self.assertEqual(0, len(form.controls))

    def test_from_bs4_optional_attrs(self):
        """
        Test parsing basic form with optional attributes defined.
        """

        form_tag = "form"
        form_attrs = {
            "name": "test1234",
            "method": "POST",
            "accept-charset": "ASCII",
            "enctype": "text/plain"
        }
        form_element = "<%s %s>" % (form_tag, " ".join("%s=\"%s\"" % (key, val)
                                                       for key, val in form_attrs.items()))

        form_element_c = "</%s>" % (form_tag)

        tag_name = "input"

        attrs = {
            "name": "test1234",
            "value": "test4321",
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        html = "".join([form_element, field, form_element_c, ])

        bs4parser = BeautifulSoup(html, "html5lib").find(form_tag)

        form = Form.from_bs4(bs4parser)

        self.assertEqual(form_attrs["name"], form.name)
        self.assertEqual(form_attrs["enctype"], form.encoding_type)
        self.assertEqual(form_attrs["method"], form.method)
        self.assertEqual(form_attrs["accept-charset"], form.accepted_charset)
        self.assertEqual(1, len(form.fields))
        self.assertEqual(0, len(form.controls))

    def test_from_bs4_skip_form_attr(self):
        """
        Verify that form fields that have a form attribute are not included
        when nested inside a form
        """

        form_tag = "form"
        form_attrs = {
            "name": "test1234",
            "method": "POST",
            "accept-charset": "ASCII",
            "enctype": "text/plain"
        }
        form_element = "<%s %s>" % (form_tag, " ".join("%s=\"%s\"" % (key, val)
                                                       for key, val in form_attrs.items()))

        form_element_c = "</%s>" % (form_tag)

        tag_name = "input"

        attrs = {
            "name": "test1234",
            "value": "test4321",
            "form": "invalid"
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        html = "".join([form_element, field, form_element_c, ])

        bs4parser = BeautifulSoup(html, "html5lib").find(form_tag)

        form = Form.from_bs4(bs4parser)

        self.assertEqual(form_attrs["name"], form.name)
        self.assertEqual(form_attrs["enctype"], form.encoding_type)
        self.assertEqual(form_attrs["method"], form.method)
        self.assertEqual(form_attrs["accept-charset"], form.accepted_charset)
        self.assertEqual(0, len(form.fields))
        self.assertEqual(0, len(form.controls))

    def test_from_bs4_capture_form_attr(self):
        """
        Verify that form fields that have a form attribute of the parent form
        node are captured.
        """

        form_tag = "form"
        form_attrs = {
            "name": "test1234",
            "method": "POST",
            "accept-charset": "ASCII",
            "enctype": "text/plain",
            "id": "form0"
        }
        form_element = "<%s %s>" % (form_tag, " ".join("%s=\"%s\"" % (key, val)
                                                       for key, val in form_attrs.items()))

        form_element_c = "</%s>" % (form_tag)

        tag_name = "input"

        attrs = {
            "name": "test1234",
            "value": "test4321",
            "form": "form0"
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        html = "".join([form_element, field, form_element_c, ])

        bs4parser = BeautifulSoup(html, "html5lib").find(form_tag)

        form = Form.from_bs4(bs4parser)

        self.assertEqual(form_attrs["name"], form.name)
        self.assertEqual(form_attrs["enctype"], form.encoding_type)
        self.assertEqual(form_attrs["method"], form.method)
        self.assertEqual(form_attrs["accept-charset"], form.accepted_charset)
        self.assertEqual(1, len(form.fields))
        self.assertEqual(0, len(form.controls))

    def test_from_dict(self):
        """
        Test parsing from dictionary.
        """

        form_dict = {
            'name': 'test1234',
            'id': None,
            'enctype': 'application/x-www-form-urlencoded',
            'method': 'GET',
            'accept-charset': 'utf-8',
            'fields': [{'name': 'test1234',
                        'type': 'text',
                        'values': [{'value': 'test4321', 'is_selected': True, 'binary_path': None}]}],
            'controls': []
        }

        form = Form.from_dict(form_dict)

        self.assertEqual(form_dict["name"], form.name)
        self.assertEqual(Form.DEFAULT_ENCODING_TYPE, form.encoding_type)
        self.assertEqual(Form.DEFAULT_METHOD, form.method)
        self.assertEqual(Form.DEFAULT_CHARSET, form.accepted_charset)
        self.assertEqual(1, len(form.fields))
        self.assertEqual(0, len(form.controls))

    def test_to_dict(self):
        """
        Test dumping to dictionary
        """

        form_tag = "form"
        form_attrs = {"name": "test1234"}
        form_element = "<%s %s>" % (form_tag, " ".join("%s=\"%s\"" % (key, val)
                                                       for key, val in form_attrs.items()))

        form_element_c = "</%s>" % (form_tag)

        tag_name = "input"

        attrs = {
            "name": "test1234",
            "value": "test4321",
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        html = "".join([form_element, field, form_element_c, ])

        bs4parser = BeautifulSoup(html, "html5lib").find(form_tag)

        form = Form.from_bs4(bs4parser).to_dict()

        self.assertEqual(form_attrs["name"], form["name"])
        self.assertEqual(Form.DEFAULT_ENCODING_TYPE, form["enctype"])
        self.assertEqual(Form.DEFAULT_METHOD, form["method"])
        self.assertEqual(Form.DEFAULT_CHARSET, form["accept-charset"])

    def test_from_bs4_form_id(self):
        """
        Test parsing basic form with elements referenced by form id.
        """

        form_tag = "form"
        form_attrs = {"name": "test1234",
                      "id": "form0000"}
        form_element = "<%s %s>" % (form_tag, " ".join("%s=\"%s\"" % (key, val)
                                                       for key, val in form_attrs.items()))

        form_element_c = "</%s>" % (form_tag)

        tag_name = "input"

        attrs = {
            "name": "test1234",
            "value": "test4321",
            "form": "form0000"
        }

        field = "<%s %s />" % (tag_name, " ".join("%s=\"%s\"" % (key, val, )
                                                  for key, val in attrs.items()))

        control = "button"
        control_attrs = {
            "name": "process",
            "type": "submit",
            "value": "process"
        }

        control_html = "<%s %s />" % (control, " ".join("%s=\"%s\"" % (key, val, )
                                                        for key, val in control_attrs.items()))

        html = "".join([field, form_element, control_html, form_element_c, ])

        bs4parser = BeautifulSoup(html, "html5lib").find(form_tag)

        form = Form.from_bs4(bs4parser)

        self.assertEqual(form_attrs["name"], form.name)
        self.assertEqual(Form.DEFAULT_ENCODING_TYPE, form.encoding_type)
        self.assertEqual(Form.DEFAULT_METHOD, form.method)
        self.assertEqual(Form.DEFAULT_CHARSET, form.accepted_charset)
        self.assertEqual(1, len(form.fields))
        self.assertEqual(1, len(form.controls))
