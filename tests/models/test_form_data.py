import unittest

from html_form_parser.models.form_data import FormData

class Test_FormData(unittest.TestCase):

    def test_new_object(self):

        obj = FormData("example", action="https://www.example.com/")

        self.assertEqual(obj.name, "example")
        self.assertEqual(obj.action, "https://www.example.com/")
        self.assertEqual(obj.method, "GET")
        self.assertEqual(obj.enctype, "multipart/form-data")
    
    def test_new_object_all_defined(self):

        obj = FormData("example", "https://www.example.com/", "POST", "multipart/garbage")

        self.assertEqual(obj.name, "example")
        self.assertEqual(obj.action, "https://www.example.com/")
        self.assertEqual(obj.method, "POST")
        self.assertEqual(obj.enctype, "multipart/garbage")
    
    def test_adding_field(self):

        obj = FormData("example", action="https://www.example.com/")

        obj.fields.append("garbage")
