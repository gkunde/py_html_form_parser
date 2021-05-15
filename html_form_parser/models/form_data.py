from typing import List

from html_form_parser.models.form_data_entry_collection import FormDataEntryCollection


class FormData:
    """
    An object for storing an HTML Form as a multipart/form-data type object.

    Properties provided:
        name: The form's "name" attribute value

        action: The form's "action" attribute

        method: The form's "method" attribute, or default of "GET"

        enctype: The form's "enctype" attribute, or default of "multipart/form-data"

        fields: A collection of the form's input fields.

    The object contains an "_attrs" collection. This collection is the source
    of the values provided in the object properties. Additionally, when
    provided a parsed object, its attributes will be loaded into this
    collection. This attribute is ideally designed for research and debugging.

    :param name: A name attributed to the form.

    :param action: The URL the form data is to be sent to.

    :param method: The HTTP verb type to use when sending the form data.

    :param enctype: The Form Data encoding type.
    """

    def __init__(self, name: str = None, action: str = None, method: str = "GET", enctype: str = "multipart/form-data"):

        self.name = name
        self.action = action
        self.method = method
        self.enctype = enctype

        self.fields = FormDataEntryCollection()

    def from_beautifulsoup(self, value: 'bs4.Tag'):
        """
        Populate the object with values from a <form /> tag parsed with
        BeautifulSoup.

        :param value: A BeautifulSoup Tag element or object providing an
            "attrs" property containing the elements attributes.
        """

        for key, value in value.attrs:

            key_lower = key.strip().lower()

            if key_lower == "name":
                self.name = value
            elif key_lower == "action":
                self.action = value
            elif key_lower == "method":
                self.method = value
            elif key_lower == "enctype":
                self.enctype = value

    def prepare_data(self) -> List[tuple]:
        """
        Generates a collection of tuples containing the field names and values
        from the collection. This is suitable for using with the requests
        library's "data" parameter.
        """

        results = [(field.name, field.value, )
                   for field in self.fields
                   if field.is_submitable and field.filename is None]

        return results

    def prepare_file_data(self) -> List[tuple]:
        """
        Genreates a collection of tuples containing the fields for files. The
        output is suitable for using with the requests library's
        "files" parameter.
        """

        results = [(field.name, (field.filename, open(field.value, "rb")), )
                   for field in self.fields
                   if field.is_submitable and field.filename is not None]

        return results
