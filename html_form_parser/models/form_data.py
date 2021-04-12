from typing import List

from .form_data_entry_collection import FormDataEntryCollection


class FormData:
    """
    An object for storing an HTML Form as a multipart/form-data type object.

    :param name: A name attributed to the form.

    :param action: The URL the form data is to be sent to.

    :param method: The HTTP verb type to use when sending the form data.

    :param enctype: The Form Data encoding type.
    """

    def __init__(self, name: str = None, action: str = None, method: str = "GET", enctype: str = "multipart/form-data"):

        self._attrs = {
            "name": name,
            "action": action,
            "method": method,
            "enctype": enctype
        }

        self._bs4_instance = None

        self.fields = FormDataEntryCollection()

    @property
    def name(self):
        return self._attrs["name"]

    @name.setter
    def name(self, value):
        self._attrs["name"] = value

    @property
    def action(self):
        return self._attrs["action"]

    @action.setter
    def action(self, value):
        self._attrs["action"] = value

    @property
    def method(self):
        return self._attrs["method"]

    @method.setter
    def method(self, value):
        self._attrs["method"] = value

    @property
    def enctype(self):
        return self._attrs["enctype"]

    @enctype.setter
    def enctype(self, value):
        self._attrs["enctype"] = value

    def from_beautifulsoup(self, value):

        for item in value.attrs.items():
            self._attrs[item[0].strip().lower()] = item[1]

    def prepare_data(self) -> List[tuple]:
        """
        Generates a collection of tuples containing the field names and values
        from the collection.
        """

        results = [(field.name, field.value, )
                   for field in self.fields
                   if field.is_submitable and field.filename is None]

        return results

    def prepare_file_data(self) -> List[tuple]:
        """
        Genreates a collection of tuples containing the fields for files
        """

        results = [(field.name, (field.filename, open(field.value, "rb")), )
                   for field in self.fields
                   if field.is_submitable and field.filename is not None]

        return results
