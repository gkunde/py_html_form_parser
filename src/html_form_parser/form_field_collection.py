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

    def __init__(self, iterable: Iterable = None):

        self.__index = []
        self.__fields = []

        self.__index_to_check = None

        if iterable is not None:
            self.extend(iterable)

    @property
    def items(self):
        """
        Returns an iterable of all the fields in the collection.
        """
        return self.__iter__

    def append(self, item: FormField):
        """
        Add item to the collection

        :param item: A FormField object to be added.
        """

        if not isinstance(item, FormField):
            self.__raise_type_error_expected(FormField, item, )

        self.__index.append((item.name, item.value, ))
        self.__fields.append(item)

    def clear(self):
        """
        Clear the contents of the collection.
        """

        self.__index.clear()
        self.__fields.clear()

    def copy(self):
        """
        A shallow copy of the fields in the collection.
        """

        return [item for item in self.__fields]

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

    def insert(self, index, form_field: FormField):
        """
        Insert a FormField object at the provided index.

        :param index: An integer index, the string field name of an existing
            entry, or a tuple of the field name and value of an existing
            entry to insert the new object at.
        
        :param form_field: The form field object to be inserted.
        """

        idx = self.__get_index(index)

        self.__index.insert(idx, (form_field.name, form_field.value, ))
        self.__fields.insert(idx, form_field)

    def pop(self, index) -> FormField:
        """
        Remove entry at given index.

        Expensive operation, this requires object indexes to rebuild.

        :para index: An integer, field name, or field name & value tuple to
            remove from the collection.
        """

        idx = self.__get_index(index)

        self.__index.pop(idx)
        return self.__fields.pop(idx)

    def sort(self):
        """
        Sorts the collection in place.
        """

        self.__fields = sorted(self.__fields, key=lambda field: (field.name, field.value, ))
        self.__index = [(field.name, field.value, ) for field in self.__fields]

        self.__index_to_check = None

    def remove(self, form_field: FormField) -> None:
        """
        Removes the referenced object from the collection.
        """

        index = (form_field.name, form_field.key, )

        self.pop(index)

    def reverse(self) -> None:
        """
        Reverses the collection in place.
        """

        self.__index.reverse()
        self.__fields.reverse()

    def __get_index(self, key) -> int:
        """
        Provides the ability to access entries in the collection with an
        integer, the name of the field, or a tuple with the name and value.
        When multiple results can be returned, the first instance is returned.

        :param key: The index or key to use for finding the index of the item.
            Can be an integer of the index, a string of the FormField.name
            property, or a tuple with the FormField.name and FormField.value.
        """

        index = None
        if isinstance(key, int):
            index = key

        elif isinstance(key, str):
            # return the first encountered element

            locations = [idx for idx, entry in enumerate(self.__index) if entry[0] == key]
            index = locations[0]

        elif isinstance(key, Iterable) and len(key) == 2:
            index = self.__index.index(key)

        return index

    def __raise_type_error_expected(self, expected, given):
        raise TypeError(self.__TYPE_ERROR_EXPECTED % (expected.__name__, given.__name__, ))

    def __len__(self) -> int:
        return len(self.__index)

    def __iter__(self) -> FormField:
        for item in self.__fields:
            yield item

    def __eq__(self, item: 'FormFieldCollection') -> bool:

        compare_to = [(field.name, field.value, ) for field in item]
        return self.__index == compare_to

    def __add__(self, form_field_collection) -> 'FormFieldCollection':
        """
        Merge two collections together, returning a new collection from the
        merge.

        :param items: The collection to be added to the this object's.
        """

        new_collection = FormFieldCollection(self)
        new_collection.extend(form_field_collection)

        return new_collection

    def __getitem__(self, key) -> FormField:
        """
        Make the object subscriptable. The items can be accessed via integer
        index, a name (only first instance will be returned), or a field name
        & value provided in a tuple.

        :param index: The index of the item to return from the collection.

        :returns: The item at the given index.
        """

        if isinstance(key, slice):
            raise TypeError("Unsupported method: 'slice'")

        if self.__index_to_check is not None:
            # Update self.__index to ensure it's value matches its companion
            # record in self.__fields.

            field = self.__fields[self.__index_to_check]
            self.__index[self.__index_to_check] = (field.name, field.value, )

            self.__index_to_check = None

        idx = self.__get_index(key)

        # Set a breadcrumb to make sure that the self.__index entry matches
        # its companion in self.__fields
        self.__index_to_check = idx

        return self.__fields[idx]

    def __setitem__(self, key, newvalue: FormField):

        idx = self.__get_index(key)

        self.pop(idx)
        self.__index.insert(idx, newvalue)
        self.__fields.insert(idx, newvalue)

    def __delitem__(self, key):
        self.pop(key)
