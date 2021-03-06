import unittest

from html_form_parser.models import form_data_field


class Test_FormDataField(unittest.TestCase):

    example_name = "example"
    example_value = "example"
    example_filename = "example.txt"
    example_filename2 = "sample.txt"
    example_filepath = "/example/path/example.txt"

    def test_new_object(self):

        obj = form_data_field.FormDataField(self.example_name)

        self.assertEqual(obj.name, self.example_name)
        self.assertIsNone(obj.value)
        self.assertIsNone(obj.filename)
        self.assertTrue(obj.is_active)

    def test_new_object_with_value(self):

        obj = form_data_field.FormDataField(self.example_name, value=self.example_value)

        self.assertEqual(obj.name, self.example_name)
        self.assertEqual(obj.value, self.example_value)
        self.assertIsNone(obj.filename)
        self.assertTrue(obj.is_active)

    def test_new_object_not_active(self):

        obj = form_data_field.FormDataField(self.example_name, is_active=False)

        self.assertEqual(obj.name, self.example_name)
        self.assertIsNone(obj.value)
        self.assertIsNone(obj.filename)
        self.assertFalse(obj.is_active)

    def test_add_file_attachement(self):

        obj = form_data_field.FormDataField(self.example_name)
        obj.add_file_attachment(self.example_filepath, None)

        self.assertEqual(obj.filename, self.example_filename)
        self.assertEqual(obj.value, self.example_filepath)

    def test_add_file_attachement_with_filename(self):

        obj = form_data_field.FormDataField(self.example_name)
        obj.add_file_attachment(self.example_filepath, self.example_filename2)

        self.assertEqual(obj.filename, self.example_filename2)
        self.assertEqual(obj.value, self.example_filepath)

    def test_remove_file_attachement(self):

        obj = form_data_field.FormDataField(self.example_name)
        obj.add_file_attachment(self.example_filepath, None)

        self.assertEqual(obj.filename, self.example_filename)
        self.assertEqual(obj.value, self.example_filepath)

        obj.remove_file_attachment()

        self.assertIsNone(obj.filename)
        self.assertIsNone(obj.value)

    def test_set_name(self):

        obj = form_data_field.FormDataField("sample")

        with self.assertRaises(AttributeError) as exp:
            obj.name = self.example_name

        self.assertEquals(str(exp.exception), "can't set attribute")

    def test_set_value(self):

        obj = form_data_field.FormDataField(self.example_name)
        obj.value = self.example_value

        self.assertEqual(obj.value, self.example_value)

    def test_set_value_with_file_attachment(self):

        obj = form_data_field.FormDataField(self.example_name)
        obj.add_file_attachment(self.example_filepath, None)

        with self.assertRaises(RuntimeError) as exp:
            obj.value = self.example_value

        self.assertEqual(str(exp.exception), "value cannot be changed when file attached.")

    def test_equal(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_value)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_value)

        self.assertEqual(obj1, obj2)

    def test_not_equal(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_value)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_filename2)

        self.assertNotEqual(obj1, obj2)

    def test_gt(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_filename2)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_value)

        self.assertGreater(obj1, obj2)

    def test_gt_equal(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_value)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_value)

        result = obj1 > obj2

        self.assertFalse(result)

    def test_ge(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_filename2)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_value)

        result = obj1 >= obj2

        self.assertTrue(result)

    def test_ge_equal(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_value)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_value)

        result = obj1 >= obj2

        self.assertTrue(result)

    def test_lt(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_value)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_filename2)

        self.assertLess(obj1, obj2)

    def test_lt_equal(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_value)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_value)

        result = obj1 < obj2

        self.assertFalse(result)

    def test_le(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_value)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_filename2)

        result = obj1 <= obj2

        self.assertTrue(result)

    def test_le_equal(self):

        obj1 = form_data_field.FormDataField(self.example_name, self.example_value)
        obj2 = form_data_field.FormDataField(self.example_name, self.example_value)

        result = obj1 <= obj2

        self.assertTrue(result)
