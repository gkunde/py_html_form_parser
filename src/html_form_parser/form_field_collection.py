from collections.abc import Iterable, MutableSequence
from typing import List

from .form_field import FormField


class FormFieldCollection(MutableSequence):
    """
    A list like collection to store and manage FormField objects. Providing
    indexable access to the FormField objects contained.

    Access to the items within the collection can be done via:

    integer of the location within the collection
        Example: form_field_collection[0]

    string providing the field name (only first instance will be returned)
        Example: form_field_collection["name_of_field"]

    tuple containing the form field name and value
        Example: form_field_collection[("name_of_field", "value_on_field", )]

    :param iterable: A collection of FormField objects to initialize with.
    """

    __TYPE_ERROR_EXPECTED = "Expected type '%s', got '%s' instead."

    def __init__(self, iterable=None):

        self.__items = []

        self.__field_name_idx = {}
        self.__field_name_value_idx = {}

        if iterable is not None:
            self.extend(iterable)

    @property
    def items(self):
        return self.__iter__

    def clear(self):
        """
        Clear the contents of the collection.
        """

        self.__items.clear()
        self.__field_name_idx.clear()
        self.__field_name_value_idx.clear()

    def index(self, index) -> int:
        """
        Returns the index location of the first instance of the item.

        :param index: An form field name or form field name value tuple to
            locate the index of the FormField object.
        """

        if isinstance(index, str) and index in self.__field_name_idx:
            return self.__field_name_idx[index]
        elif isinstance(index, Iterable) and index in self.__field_name_value_idx:
            return self.__field_name_value_idx[index]
        else:
            raise ValueError("%s is not in list" % (index, ))

    def pop(self, index=None) -> FormField:
        """
        Remove entry at given index.

        Expensive operation, this requires object indexes to rebuild.

        :para index: An integer, field name, or field name & value tuple to
            remove from the collection.
        """

        idx = None
        if index is None:
            idx = len(self) - 1
        elif isinstance(index, int):
            idx = index
        elif isinstance(index, str):
            idx = self.__field_name_idx[index]
        elif isinstance(index, Iterable) and len(index) == 2:
            idx = self.__field_name_value_idx[index]
        else:
            raise IndexError("Out of range.")

        item = self.__items.pop(idx)

        for key, value in self.__field_name_idx.items():
            if value >= idx:
                self.__field_name_idx[key] -= 1

        for key, value in self.__field_name_value_idx.items():
            if value >= idx:
                self.__field_name_value_idx[key] -= 1

        return item

    def insert(self, index, item):
        """
        Insert a field at a specific index in the collection.

        NOTE: The index must of an existing entry in the collection, not the
        from the FormField you are attempting to add.

        This is an operation requires a rebuild of object indexes, use
        sparingly.

        :param index: An integer, field name, or field name & value tuple to
            insert the given object at.

        :param item: The FormField value to be inserted.
        """

        if not isinstance(item, FormField):
            self.__raise_type_error_expected(FormField, item)

        idx = None
        if isinstance(index, int):
            idx = index
        elif isinstance(index, str):
            idx = self.__field_name_idx[index]
        elif isinstance(index, Iterable) and len(index) == 2:
            idx = self.__field_name_value_idx[index]
        else:
            raise IndexError("Out of range.")

        self.__items.insert(index, item)

        for key, value in self.__field_name_idx.items():
            if value >= idx:
                self.__field_name_value_idx[key] += 1

        for key, value in self.__field_name_value_idx.items():
            if value >= idx:
                self.__field_name_value_idx[key] += 1

        self.__field_name_idx[item.name] = idx

        for val in item.values:
            self.__field_name_value_idx[(item.name, val.value, )] = idx

    def append(self, item: FormField):
        """
        Add item to the collection

        :param item: A FormField object to be added.
        """

        if not isinstance(item, FormField):
            self.__raise_type_error_expected(FormField, item, )

        new_idx = len(self)

        if item.name not in self.__field_name_idx:
            self.__field_name_idx[item.name] = new_idx

        key_value = (item.name, item.value, )
        if key_value not in self.__field_name_idx:
            self.__field_name_value_idx[key_value] = new_idx

        self.__items.append(item)

    def extend(self, items: List[FormField]):
        """
        Append another collection of FormFields to this collection.

        :param items: A collection of FormFields contained in a list or
            another FormFieldsCollection object.
        """

        if isinstance(items, (Iterable, FormFieldCollection, )):
            for item in items:
                self.append(item)

        else:
            self.__raise_type_error_expected(Iterable, items)

    def __len__(self):
        return len(self.__items)

    def __iter__(self):
        for item in self.__items:
            yield item

    def __eq__(self, item):
        raise NotImplementedError()

    def __add__(self, items) -> 'FormFieldCollection':
        """
        Merge two collections together, returning a new collection from the
        merge.

        :param items: The collection to be added to the this object's.
        """

        new_collection = FormFieldCollection(self)
        new_collection.extend(items)

        return new_collection

    def __getitem__(self, index) -> FormField:
        """
        Make the object subscriptable. The items can be accessed via integer
        index, a name (only first instance will be returned), or a field name
        & value provided in a tuple.

        :param index: The index of the item to return from the collection.

        :returns: The item at the given index.
        """

        if isinstance(index, int):
            return self.__items[index]
        elif isinstance(index, str):
            return self.__items[self.__field_name_idx[index]]
        elif isinstance(index, Iterable) and len(index) == 2:
            return self.__items[self.__field_name_value_idx[index]]
        elif isinstance(index, slice):
            raise TypeError("Unsupported method: 'slice'")
        else:
            raise IndexError("Out of range.")

    def __setitem__(self, key, newvalue):
        raise NotImplementedError()

    def __delitem__(self, key):
        self.pop(key)

    def __raise_type_error_expected(self, expected, given):
        raise TypeError(self.__TYPE_ERROR_EXPECTED % (expected.__name__, given.__name__, ))
