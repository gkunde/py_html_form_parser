import unittest

from html_form_parser import Form


class Test_Form(unittest.TestCase):

    def test_init(self):
        """
        """

        html_header = """<html><head><title>Test Form</title></head><body>"""
        html_trailer = """</body></html>"""

        form_tag = "form"
        form_attrs = {"name": "test1234",
                      "id": "form0000",
                      "action": "https://www.example.com/",
                      "method": "GET",
                      "enctype": "multipart/form-data"}
        form_header = "<%s %s>" % (form_tag, " ".join("%s=\"%s\"" % (key, val)
                                                      for key, val in form_attrs.items()))
        form_trailer = "</%s>" % (form_tag, )

        field0_tag = "input"
        field0_attrs = {
            "name": "test1234",
            "value": "test4321",
        }

        field0 = "<%s %s />" % (field0_tag, " ".join("%s=\"%s\"" % (key, val, )
                                                     for key, val in field0_attrs.items()))

        control0_tag = "button"
        control0_attrs = {
            "name": "process",
            "type": "submit",
            "value": "process"
        }

        control0 = "<%s %s />" % (control0_tag, " ".join("%s=\"%s\"" % (key, val, )
                                                         for key, val in control0_attrs.items()))

        html = "".join((
            html_header,
            form_header,
            field0,
            control0,
            form_trailer,
            html_trailer
        ))

        form_manager = Form(html)

        self.assertEqual(form_attrs["action"], form_manager.action)
        self.assertEqual(form_attrs["enctype"], form_manager.enctype)
        self.assertEqual(form_attrs["method"], form_manager.method)
        self.assertEqual(form_attrs["name"], form_manager.name)

        self.assertEqual(2, len(form_manager.fields))

    def test_parsing_attribute_name(self):

        form_name = "testform678"
        html = "<form name=\"%s\"></form>" % (form_name, )

        form = Form(html)

        self.assertEqual(form_name, form.name)

    def test_parsing_attribute_method(self):

        form_method = "POST"
        html = "<form method=\"%s\"></form>" % (form_method, )

        form = Form(html)

        self.assertEqual(form_method, form.method)

    def test_parsing_attribute_action(self):

        form_action = "https://www.example.com/"
        html = "<form action=\"%s\" />" % (form_action, )
        form = Form(html)

        self.assertEqual(form_action, form.action)

    def test_parsing_optional_attribute(self):

        form_attribute = "id"
        form_id = "testform746"
        html = "<form %s=\"%s\"></form>" % (form_attribute, form_id, )

        form = Form(html)

        self.assertIn(form_attribute, form._attributes)
        self.assertEqual(form_id, form._attributes["id"])

    def test_fetching_form_by_name(self):

        form_0 = "form0"
        form_1 = "form1"
        html = "<form name=\"%s\"></form><form name=\"%s\"></form>" % (form_0, form_1, )

        form = Form(html, name=form_1)

        self.assertEquals(form_1, form.name)
        self.assertNotEquals(form_0, form.name)

    def test_readonly_attribute(self):

        html = "<form " \
            "name=\"example\" " \
            "id=\"exmaple\" "\
            "action=\"https://www.example.com/\" " \
            "enctype=\"multipart/form-data\" " \
            "method=\"POST\"></form>"

        form = Form(html)

        with self.assertRaises(AttributeError) as exp:
            form.name = "new_example"

        self.assertEquals("can't set attribute", str(exp.exception))
    
    def test_form_parse_stops_when_parser_is_found(self):

        html = "<form " \
            "name=\"example\" " \
            "id=\"example\" " \
            "method=\"POST\">" \
            "<select name=\"exampleSelect\">" \
            "<option value=\"001\">Option 1</option>" \
            "<option value=\"002\">Option 2</option>" \
            "</select></form>"
        
        form = Form(html)

        data = list(form.fields)

        self.assertEqual(2, len(data))
