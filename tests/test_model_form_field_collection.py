import unittest

# from html_form_parser.form_field import FormField
from html_form_parser.elements import FormElement
from html_form_parser.form_field_collection import FormFieldCollection


class Test_Model_FormFieldCollection(unittest.TestCase):

    _formfield_singlevalue = FormElement("testfield", value="testvalue")

    def test_init(self):

        col = FormFieldCollection([self._formfield_singlevalue, ])

        self.assertEqual(1, len(col))

    def test_append(self):

        col = FormFieldCollection()
        col.append(self._formfield_singlevalue)

        self.assertEqual(1, len(col))

    def test_extend(self):

        extender = [self._formfield_singlevalue,
                    self._formfield_singlevalue, ]

        col = FormFieldCollection()
        col.extend(extender)

        self.assertEqual(len(extender), len(col))

    def test_add(self):

        col0 = FormFieldCollection([self._formfield_singlevalue, ])
        col1 = FormFieldCollection([self._formfield_singlevalue, ])

        col = col0 + col1

        self.assertEqual(2, len(col))

    def test_iterate(self):

        col = FormFieldCollection([self._formfield_singlevalue,
                                   self._formfield_singlevalue, ])

        count = len(col)
        idx = 0
        for _ in col:
            idx += 1

        self.assertEqual(count, idx)

    def test_items_iterate(self):

        col = FormFieldCollection([self._formfield_singlevalue,
                                   self._formfield_singlevalue, ])

        count = len(col)
        idx = 0
        for _ in col.items():
            idx += 1

        self.assertEqual(count, idx)

    def test_items(self):

        col = FormFieldCollection([self._formfield_singlevalue, ])

        new_col = list(col)

        self.assertEqual(len(col), len(new_col))

    def test_subscriptable_by_name(self):

        col = FormFieldCollection([self._formfield_singlevalue, ])

        item = col[self._formfield_singlevalue.name]

        self.assertEqual(col[0], item)

    def test_subscriptable_by_name_value(self):

        col = FormFieldCollection([self._formfield_singlevalue, ])

        item = col[(self._formfield_singlevalue.name,
                    self._formfield_singlevalue.value, )]

        self.assertEqual(col[0], item)

    def test_slice(self):

        col = FormFieldCollection([self._formfield_singlevalue,
                                   self._formfield_singlevalue,
                                   self._formfield_singlevalue, ])

        self.assertRaises(TypeError, col.__getitem__, slice(1, None, None))
