from collections.abc import Iterable, MutableSequence
from typing import List

from html_form_parser.models.form_data_entry import FormDataEntry


class FormDataEntryCollection(MutableSequence):
    """
    A collection of FormDataField objects. Providing methods for locating
    entries in the collection by name, or name and value.

    :param fields: A collection of fields to add to this instance.
    """

    def __init__(self, fields: List[FormDataEntry] = None):

        self.__fields = []

        # Indexes used by the index() method to optimize searching for fields.
        self.__field_name_index = {}
        self.__field_name_value_index = {}

        # A flag to let the index() method know that it needs to refresh the
        # index before doing a lookup.
        self.__is_dirty = False

        if fields is not None:
            self.extend(fields)

    def index_by_name(self, name: str) -> int:
        """
        Return zero-based index of the first field providing a matching name.

        :param name: A "name" to match in the collection of FormDataFields.
        """

        self.__refresh_indexes()

        return self.__field_name_index[name][0]

    def index_by_name_value(self, name: str, value: str) -> int:
        """
        Return zero-based index of the first field providing a matching name
        and value.

        :param name: A "name" to match in the collection of FormDataFields.

        :param value: A "value" to match in the collection of
            FormDataFields.
        """

        self.__refresh_indexes()

        return self.__field_name_value_index[(name, value, )]

    def insert(self, index: int, value: FormDataEntry):
        """
        Inserts a FormDataField at the given index. Note this is a very
        intensive operation, as each insert triggers a rebuild of the
        object's indexes.

        :param index: The location in the collection to insert the given
            value at.

        :param value: The value to be inserted into the collection.
        """

        self.__is_dirty = True

        self.__fields.insert(index, value)

    def sort(self, key=None, reverse=False):
        """
        Sorts the collection of fields in place.
        """

        self.__is_dirty = True

        self.__fields.sort(key=key, reverse=reverse)

    def __add_field_to_index(self, index: int, field: FormDataEntry):
        """
        Create a new entry to the indexes.

        :param index: The location of the field in the collection.

        :param field: The FormDataField object to obtain key values from.
        """

        if field.name not in self.__field_name_index:
            self.__field_name_index[field.name] = []

        self.__field_name_index[field.name].append(index)
        self.__field_name_index[field.name].sort()

        key = (field.name, field.value, )
        if key not in self.__field_name_value_index:
            self.__field_name_value_index[key] = index

    def __refresh_indexes(self):
        """
        Rebuilds the indexes.
        """

        if not self.__is_dirty:
            # The collection hasn't been marked dirty, there is nothing to do.
            return

        self.__field_name_index = {}
        self.__field_name_value_index = {}

        for index, item in enumerate(self.__fields):
            self.__add_field_to_index(index, item)

        self.__is_dirty = False

    def __getitem__(self, index: int) -> FormDataEntry:
        """
        Fetches a FormDataField from the collection using the given index.
        """

        self.__is_dirty = True

        return self.__fields[index]

    def __setitem__(self, index: int, value: FormDataEntry):
        """
        Sets the FormDataField in the collection to the new value.

        :param index: The location to update with the given value.

        :param new_value: A FormDataField to replace the current
            FormDataField found at the given index.
        """

        self.__is_dirty = True

        self.__fields[index] = value

    def __delitem__(self, index: int):
        """
        Removes a FormDataField from the collection.

        :param index: The location to update with the given value.
        """

        self.__is_dirty = True

        del self.__fields[index]

    def __len__(self) -> int:
        """
        Return the number of entries in the collection.
        """

        return len(self.__fields)
