import unittest

from html_form_parser.models.form_data_field import FormDataField
from html_form_parser.models.form_data_field_collection import FormDataFieldCollection


class Test_FormDataFieldCollection(unittest.TestCase):

    field1 = FormDataField("example1", "test1234")
    field2 = FormDataField("example2", "test5678")

    def test_new_object(self):

        obj1 = FormDataFieldCollection()

        self.assertEqual(len(obj1), 0)

    def test_new_object_with_fields(self):

        obj1 = FormDataFieldCollection([self.field1, self.field2, ])

        self.assertEqual(len(obj1), 2)

    def test_index_name_only(self):

        obj = FormDataFieldCollection()
        obj.extend([self.field2, self.field1, ])

        self.assertEqual(obj.index(self.field1.name), 1)

    def test_index_name_value(self):

        obj = FormDataFieldCollection()
        obj.extend([self.field2, self.field1, ])

        self.assertEqual(obj.index(self.field1.name, self.field1.value), 1)

    def test_sort(self):

        obj = FormDataFieldCollection()
        obj.extend([self.field2, self.field1, ])
        obj.sort()

        self.assertEqual(len(obj), 2)
        self.assertEqual(obj[0], self.field1)
        self.assertEqual(obj[1], self.field2)
