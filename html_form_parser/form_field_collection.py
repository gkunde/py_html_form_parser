from collections.abc import Iterable, MutableSequence
from typing import List

from .elements import FormElement


class FormFieldCollection(MutableSequence):
    """
    A list like collection to store and manage FormElement objects. Providing
    indexable access to the FormElement objects contained.

    Access to the items within the collection can be done via:

    integer of the location within the collection
        Example: form_field_collection[0]

    string providing the field name (only first instance will be returned)
        Example: form_field_collection["name_of_field"]

    tuple containing the form field name and value
        Example: form_field_collection[("name_of_field", "value_on_field", )]

    :param iterable: A collection of FormElement objects to initialize with.
    """

    __type_error_expected = "Expected type '%s', got '%s' instead."

    def __init__(self, iterable: List[FormElement] = None):

        self.__fields = []

        # This indicates which item from the collection was last accessed, and
        # its name and value need to be checked for an update.
        self.__index_to_check = None

        # These indexes are intended to provide a lookup for the objects
        # stored in self.__fields. One to enable look-ups by a FormElement.name
        # attribute, the other to perform look-ups by FormElement.name and
        # FormElement.value.
        self.__index_name = {}
        self.__index_name_value = {}

        if iterable is not None:
            self.extend(iterable)

    @property
    def items(self):
        """
        Returns an iterable of all the fields in the collection.
        """
        return self.__iter__

    def append(self, form_field: FormElement):
        """
        Add item to the collection

        :param form_field: A FormElement object to be added.
        """

        if not isinstance(form_field, FormElement):
            self.__raise_type_error_expected(FormElement, form_field, )

        new_index = len(self.__fields)
        if form_field.name not in self.__index_name:
            self.__index_name[form_field.name] = new_index

        key = (form_field.name, form_field.value, )
        if key not in self.__index_name_value:
            self.__index_name_value[key] = new_index

        self.__fields.append(form_field)

    def clear(self):
        """
        Clear the contents of the collection.
        """

        self.__fields.clear()

        self.__refresh_index()

    def copy(self):
        """
        A shallow copy of the fields in the collection.
        """

        return [item for item in self.__fields]

    def extend(self, form_fields: List[FormElement]):
        """
        Append another collection of FormElements to this collection.

        :param form_fields: A collection of FormElements contained in a list or
            another FormElementsCollection object.
        """

        if isinstance(form_fields, (Iterable, FormFieldCollection, )):
            for item in form_fields:
                self.append(item)

        else:
            self.__raise_type_error_expected(Iterable, form_fields)

    def index(self, key) -> int:
        """
        Return the index value based on the provided key.

        A key can be:
            integer - Will just echo back the value
            string - Will refer to the "name" property of the FormElement objects
                in the collection.
            tuple[string, string] - Will refer to the "name" and "value"
                properties of the FormElement objects.
            FormElement - Will find the matching FormElement object.

        :param key: The item to find
        """

        if isinstance(key, slice):
            raise TypeError("slice not supported")
        elif isinstance(key, int):
            return key
        elif isinstance(key, str):
            return self.__index_name[key]
        elif isinstance(key, Iterable) and len(key) == 2:
            return self.__index_name_value[key]
        elif isinstance(key, FormElement):
            return self.__fields.index(key)

    def insert(self, key, form_field: FormElement):
        """
        Insert a FormElement object at the provided index.

        :param key: An integer index, the string field name of an existing
            entry, or a tuple of the field name and value of an existing
            entry to insert the new object at.

        :param form_field: The form field object to be inserted.
        """

        idx = self.index(key)

        self.__fields.insert(idx, form_field)

        self.__index_name[form_field.name] = idx
        self.__index_name_value[(form_field.name, form_field.value, )] = idx

    def pop(self, key) -> FormElement:
        """
        Remove entry at given index.

        Expensive operation, this requires object indexes to rebuild.

        :para key: An integer, field name, or field name & value tuple to
            remove from the collection.
        """

        idx = self.index(key)

        form_field = self.__fields.pop(idx)

        # Remove from the index, do not raise error if not found.
        self.__index_name.pop(form_field.name, None)
        self.__index_name_value.pop((form_field.name, form_field.value, ), None)

        return form_field

    def sort(self):
        """
        Sorts the collection in place.
        """

        self.__fields = sorted(self.__fields, key=lambda field: (field.name, field.value, ))

        self.__refresh_index()

    def remove(self, form_field: FormElement) -> None:
        """
        Removes the referenced object from the collection.
        """

        self.pop(form_field)

    def reverse(self) -> None:
        """
        Reverses the collection in place.
        """

        self.__fields.reverse()

        self.__refresh_index()

    def __refresh_index(self):
        """
        Refreshes the indexes.
        """

        self.__index_name.clear()
        self.__index_name_value.clear()

        for index in range(0, len(self.__fields)):
            self.__update_index(index)

        self.__index_to_check = None

    def __update_index(self, key):
        """
        Update the indexes using the values found in self.__fields[key]

        :param key: Integer index of the FormElement object create index for.
        """

        form_field = self.__fields[key]

        if form_field.name not in self.__index_name:
            self.__index_name[form_field.name] = key

        key = (form_field.name, form_field.value, )
        if key not in self.__index_name_value:
            self.__index_name_value[key] = key

        # Reset the breadcrumb, the key has been updated/refreshed.
        if self.__index_to_check == key:
            self.__index_to_check = None

    def __raise_type_error_expected(self, expected, given):
        raise TypeError(self.__type_error_expected % (expected.__name__, type(given).__name__, ))

    def __len__(self) -> int:
        return len(self.__fields)

    def __iter__(self) -> FormElement:

        for index, item in enumerate(self.__fields):

            self.__index_to_check = index

            yield item

            self.__update_index(index)

    def __eq__(self, compare_to: 'FormElementCollection') -> bool:

        return not self.__ne__(compare_to)

    def __ne__(self, compare_to: 'FormElementCollection') -> bool:

        if len(self) == len(compare_to):
            return False

        for index, form_field in enumerate(self):
            if form_field == compare_to[index]:
                return False

        return True

    def __add__(self, iterable: List[FormElement]) -> 'FormElementCollection':
        """
        Merge two collections together, returning a new collection from the
        merge.

        :param iterable: The collection to be added to the this object's.
        """

        new_collection = FormFieldCollection(self)
        new_collection.extend(iterable)

        return new_collection

    def __getitem__(self, key) -> FormElement:
        """
        Make the object subscriptable. The items can be accessed via integer
        index, a name (only first instance will be returned), or a field name
        & value provided in a tuple.

        :param key: The index of the item to return from the collection.

        :returns: The item at the given index.
        """

        index = self.index(key)

        if self.__index_to_check is not None:
            self.__update_index(self.__index_to_check)

        # Set a breadcrumb to make sure that the self.__index entry matches
        # its companion in self.__fields
        self.__index_to_check = index

        return self.__fields[index]

    def __setitem__(self, key, newvalue: FormElement):
        """
        Set an object at the given "key" or indexed location.

        :param key: the index or key of the record to be set.
        """

        idx = self.index(key)

        self.remove(idx)

        self.__fields.insert(idx, newvalue)
        self.__update_index(idx)

    def __delitem__(self, key):
        """
        Remove the object at the given "key" or indexed location.

        :param key: The idnex or key of the record to be deleted.
        """

        self.remove(key)
