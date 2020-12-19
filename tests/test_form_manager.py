import unittest

from html_form_parser import FormManager


class Test_FormManager(unittest.TestCase):

    def test_init(self):
        """
        """

        html_header = """<html><head><title>Test Form</title></head><body>"""
        html_trailer = """</body></html>"""

        form_tag = "form"
        form_attrs = {"name": "test1234",
                      "id": "form0000"}
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

        form_manager = FormManager(html)

        self.assertEqual(1, len(form_manager.forms))
        self.assertEqual(2, len(form_manager.forms[0].fields))

    def test_parse(self):
        """
        """

        html_header = """<html><head><title>Test Form</title></head><body>"""
        html_trailer = """</body></html>"""

        form_tag = "form"
        form_attrs = {"name": "test1234",
                      "id": "form0000"}
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

        forms = FormManager.parse_forms(html)

        self.assertEqual(1, len(forms))
        self.assertEqual(2, len(forms[0].fields))

    def test_get_form_by_name(self):

        html_header = """<html><head><title>Test Form</title></head><body>"""
        html_trailer = """</body></html>"""

        form_tag = "form"
        form_attrs = {"name": "test1234",
                      "id": "form0000"}
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

        form_manager = FormManager(html)

        self.assertEqual(1, len(form_manager.forms))
        self.assertEqual(form_attrs["name"], form_manager.get_form_by_name(form_attrs["name"]).name)

    def test_get_form_by_name_exception(self):

        html_header = """<html><head><title>Test Form</title></head><body>"""
        html_trailer = """</body></html>"""

        form_tag = "form"
        form_attrs = {"name": "test1234",
                      "id": "form0000"}
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

        form_manager = FormManager(html)

        self.assertRaises(IndexError, form_manager.get_form_by_name, "invalid")

    def test_get_form_by_id(self):

        html_header = """<html><head><title>Test Form</title></head><body>"""
        html_trailer = """</body></html>"""

        form_tag = "form"
        form_attrs = {"name": "test1234",
                      "id": "form0000"}
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

        form_manager = FormManager(html)

        self.assertEqual(1, len(form_manager.forms))
        self.assertEqual(form_attrs["id"], form_manager.get_form_by_id(form_attrs["id"]).id)

    def test_get_form_by_id_exception(self):

        html_header = """<html><head><title>Test Form</title></head><body>"""
        html_trailer = """</body></html>"""

        form_tag = "form"
        form_attrs = {"name": "test1234",
                      "id": "form0000"}
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

        form_manager = FormManager(html)

        self.assertRaises(IndexError, form_manager.get_form_by_id, "invalid")
