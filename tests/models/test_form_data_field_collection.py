import unittest

from html_form_parser.models.form_data_entry import FormDataEntry
from html_form_parser.models.form_data_entry_collection import FormDataEntryCollection


class Test_FormDataFieldCollection(unittest.TestCase):

    field1 = FormDataEntry("example1", "test1234")
    field2 = FormDataEntry("example2", "test5678")

    def test_new_object(self):

        obj1 = FormDataEntryCollection()

        self.assertEqual(len(obj1), 0)

    def test_new_object_with_fields(self):

        obj1 = FormDataEntryCollection([self.field1, self.field2, ])

        self.assertEqual(len(obj1), 2)

    def test_index_name_only(self):

        obj = FormDataEntryCollection()
        obj.extend([self.field2, self.field1, ])

        self.assertEqual(obj.index_by_name(self.field1.name), 1)

    def test_index_name_value(self):

        obj = FormDataEntryCollection()
        obj.extend([self.field2, self.field1, ])

        self.assertEqual(obj.index_by_name_value(self.field1.name, self.field1.value), 1)

    def test_sort(self):

        obj = FormDataEntryCollection()
        obj.extend([self.field2, self.field1, ])
        obj.sort()

        self.assertEqual(len(obj), 2)
        self.assertEqual(obj[0], self.field1)
        self.assertEqual(obj[1], self.field2)

    def test_clear(self):

        obj = FormDataEntryCollection()
        obj.extend([self.field2, self.field1, ])
        obj.clear()

        self.assertEqual(len(obj), 0)

    def test_insert(self):

        obj = FormDataEntryCollection()
        obj.extend([self.field2, self.field1, ])
        obj.insert(1, self.field1)

        self.assertEqual(len(obj), 3)
