import unittest

from html_form_parser.models import form_data_entry


class Test_FormDataField(unittest.TestCase):

    example0_name = "452e5de9-e0f2-4754-9fa5-a8d04af600ae"
    example0_value = "5e34eb53-c4e5-43de-9630-179830a150c5"
    example0_filename = "f8663ede-e712-43d6-817f-ac2e624150fd"

    example1_name = "452e5de9-e0f2-4754-9fa5-a8d04af600ae"
    example1_value = "5e34eb53-c4e5-43de-9630-179830a150c5"
    example1_filename = "f8663ede-e712-43d6-817f-ac2e624150fd"

    example2_name = "0f5a6832-8171-4fd7-ada6-edb2c59fff17"
    example2_value = "f70da385-aa33-4347-8b4b-09ea410575f5"
    example2_filename = "1191a284-e509-4285-91a1-b747f41d87ec"

    def test_new_object(self):

        obj = form_data_entry.FormDataEntry()

        self.assertIsNone(obj.name)
        self.assertIsNone(obj.value)
        self.assertIsNone(obj.filename)
        self.assertTrue(obj.is_submitable)

    def test_new_object_with_name(self):

        obj = form_data_entry.FormDataEntry(name=self.example0_name)

        self.assertEqual(obj.name, self.example0_name)

    def test_new_object_with_value(self):

        obj = form_data_entry.FormDataEntry(value=self.example0_value)

        self.assertEqual(obj.value, self.example0_value)

    def test_new_object_with_filename(self):

        obj = form_data_entry.FormDataEntry(filename=self.example0_filename)

        self.assertEqual(obj.filename, self.example0_filename)

    def test_new_object_with_submitable(self):

        obj = form_data_entry.FormDataEntry(is_submitable=False)

        self.assertFalse(obj.is_submitable)

    def test_set_name(self):

        obj = form_data_entry.FormDataEntry()
        obj.name = self.example0_name

        self.assertEqual(obj.name, self.example0_name)

    def test_set_value(self):

        obj = form_data_entry.FormDataEntry()
        obj.value = self.example0_value

        self.assertEqual(obj.value, self.example0_value)

    def test_set_filename(self):

        obj = form_data_entry.FormDataEntry()
        obj.filename = self.example0_filename

        self.assertEqual(obj.filename, self.example0_filename)

    def test_set_submitable(self):

        obj = form_data_entry.FormDataEntry()
        obj.is_submitable = False

        self.assertFalse(obj.is_submitable)

    def test_positional(self):

        obj = form_data_entry.FormDataEntry(
            self.example0_name,
            self.example0_value,
            self.example0_filename)

        self.assertEqual(obj.name, self.example0_name)
        self.assertEqual(obj.value, self.example0_value)
        self.assertEqual(obj.filename, self.example0_filename)

    def test_eq(self):

        obj0 = form_data_entry.FormDataEntry(
            self.example0_name,
            self.example0_value,
            self.example0_filename)

        obj1 = form_data_entry.FormDataEntry(
            self.example1_name,
            self.example1_value,
            self.example1_filename)

        result = obj0 == obj1

        self.assertTrue(result)

    def test_ne(self):

        obj0 = form_data_entry.FormDataEntry(
            self.example0_name,
            self.example0_value,
            self.example0_filename)

        obj1 = form_data_entry.FormDataEntry(
            self.example2_name,
            self.example2_value,
            self.example2_filename)

        result = obj0 != obj1

        self.assertTrue(result)

    def test_le(self):

        obj0 = form_data_entry.FormDataEntry(
            self.example0_name,
            self.example0_value,
            self.example0_filename)

        obj1 = form_data_entry.FormDataEntry(
            self.example2_name,
            self.example2_value,
            self.example2_filename)

        result = obj1 <= obj0

        self.assertTrue(result)

    def test_ge(self):

        obj0 = form_data_entry.FormDataEntry(
            self.example0_name,
            self.example0_value,
            self.example0_filename)

        obj1 = form_data_entry.FormDataEntry(
            self.example2_name,
            self.example2_value,
            self.example2_filename)

        result = obj0 >= obj1

        self.assertTrue(result)

    def test_le_equal_values(self):

        obj0 = form_data_entry.FormDataEntry(
            self.example0_name,
            self.example0_value,
            self.example0_filename)

        obj1 = form_data_entry.FormDataEntry(
            self.example1_name,
            self.example1_value,
            self.example1_filename)

        result = obj0 <= obj1

        self.assertTrue(result)

    def test_ge_equal_values(self):

        obj0 = form_data_entry.FormDataEntry(
            self.example0_name,
            self.example0_value,
            self.example0_filename)

        obj1 = form_data_entry.FormDataEntry(
            self.example1_name,
            self.example1_value,
            self.example1_filename)

        result = obj0 >= obj1

        self.assertTrue(result)

    def test_lt(self):

        obj0 = form_data_entry.FormDataEntry(
            self.example0_name,
            self.example0_value,
            self.example0_filename)

        obj1 = form_data_entry.FormDataEntry(
            self.example2_name,
            self.example2_value,
            self.example2_filename)

        result = obj1 < obj0

        self.assertTrue(result)

    def test_gt(self):

        obj0 = form_data_entry.FormDataEntry(
            self.example0_name,
            self.example0_value,
            self.example0_filename)

        obj1 = form_data_entry.FormDataEntry(
            self.example2_name,
            self.example2_value,
            self.example2_filename)

        result = obj0 > obj1

        self.assertTrue(result)

    def test_lt_equal_values(self):

        obj0 = form_data_entry.FormDataEntry(
            "self.example0_name",
            "self.example0_value",
            "self.example0_filename")

        obj1 = form_data_entry.FormDataEntry(
            "self.example1_name",
            "self.example1_value",
            "self.example1_filename")

        result = obj0 < obj1

        self.assertTrue(result)

    def test_gt_equal_values(self):

        obj0 = form_data_entry.FormDataEntry(
            "self.example0_name",
            "self.example0_value",
            "self.example0_filename")

        obj1 = form_data_entry.FormDataEntry(
            "self.example1_name",
            "self.example1_value",
            "self.example1_filename")

        result = obj1 > obj0

        self.assertTrue(result)
