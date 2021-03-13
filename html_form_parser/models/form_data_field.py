import os


class FormDataField:
    """
    Stores the field name and value for a form post field. To attach a file
    to the field, use the add_file_attachment.

    If a file attachment has been added to the object, the "value" property
    will become read-only. The file attachement must be removed before the
    value can be changed.

    :param name: The form data field name

    :param value: The form data field value or file attachment contents.
    """

    def __init__(self, name: str, value: str = None, is_active: bool = True):

        self.__name = name

        self.__value = value

        self.__filename = None

        self.is_active = is_active

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):

        if self.filename:
            raise RuntimeError("value cannot be changed when file attached.")

        self.__value = value

    @property
    def filename(self) -> str:
        return self.__filename

    def add_file_attachment(self, filepath: str, filename: str = None):
        """
        Add a file attachment to the "file" HTML form input field.

        :param path: A file path to the file to attach.

        :param filename: An alternative file name to upload the file as.
            If none is provided, the filename will be extracted from the file
            path.
        """

        self.value = filepath
        self.__filename = filename

        if not filename:
            self.__filename = os.path.basename(filepath)

    def remove_file_attachment(self):
        """
        Removes the file attachement, setting object value to None
        """

        self.__filename = None
        self.value = None

    def __eq__(self, other: 'FormDataField'):
        """
        Determine if this object and the other object are the same.

        :param other: A FormDataField object to compare to.
        """

        if not isinstance(other, FormDataField):
            return NotImplemented

        return (self.name, self.value, self.filename, ) == (other.name, other.value, other.filename, )

    def __ne__(self, other: 'FormDataField'):
        """
        Determine if this object and the other object are not the same.

        :param other: A FormDataField object to compare to.
        """

        return not self.__eq__(other)

    def __lt__(self, other: 'FormDataField'):
        """
        Determine if this object is less than another object.

        :param other: A FormDataField object to compare to.
        """

        if not isinstance(other, FormDataField):
            return NotImplemented

        return (self.name, self.value, self.filename, ) < (other.name, other.value, other.filename, )

    def __le__(self, other: 'FormDataField'):
        """
        Determine if this object is less than or equal to another object.

        :param other: A FormDataField object to compare to.
        """

        if self == other:
            return True

        return self < other

    def __gt__(self, other: 'FormDataField'):
        """
        Determine if this object is greater than another object.

        :param other: A FormDataField object to compare to.
        """

        if not isinstance(other, FormDataField):
            return NotImplemented

        return (self.name, self.value, self.filename, ) > (other.name, other.value, other.filename, )

    def __ge__(self, other: 'FormDataField'):
        """
        Determine if this object is greater than or equal to another object.

        :param other: A FormDataField object to compare to.
        """

        if self == other:
            return True

        return self > other
