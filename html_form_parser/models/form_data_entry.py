

class FormDataEntry:
    """
    Stores the field name and value for a form post field. To attach a file
    to the field, use the add_file_attachment.

    If a file attachment has been added to the object, the "value" property
    will become read-only. The file attachement must be removed before the
    value can be changed.

    :param name: The form data field name

    :param value: The form data field value or file attachment contents.

    :param filename: A filename used if file data is stored in value.

    :param is_submitable: A flag to indicate if a field should be included
        with a HTTP post.
    """

    def __init__(self, name: str = None, value: str = None, filename: str = None, is_submitable: bool = True):

        self.content_type = "form-data"

        self.name = name
        self.value = value
        self.filename = filename
        self.is_submitable = is_submitable

    def __eq__(self, other: 'FormDataField'):
        """
        Determine if this object and the other object are the same.

        :param other: A FormDataField object to compare to.
        """

        if not isinstance(other, FormDataEntry):
            return NotImplemented

        return (self.name, self.value, self.filename, ) == (other.name, other.value, other.filename, )

    def __ne__(self, other: 'FormDataField'):
        """
        Determine if this object and the other object are not the same.

        :param other: A FormDataField object to compare to.
        """

        return not self.__eq__(other)

    def __gt__(self, other: 'FormDataField'):
        """
        Determine if this object is greater than another object.

        :param other: A FormDataField object to compare to.
        """

        if not isinstance(other, FormDataEntry):
            return NotImplemented

        return (self.name, self.value, self.filename, ) > (other.name, other.value, other.filename, )

    def __ge__(self, other: 'FormDataField'):
        """
        Determine if this object is greater than or equal to another object.

        :param other: A FormDataField object to compare to.
        """

        return (self.__eq__(other) or self.__gt__(other))

    def __lt__(self, other: 'FormDataField'):
        """
        Determine if this object is less than another object.

        :param other: A FormDataField object to compare to.
        """

        return (not self.__eq__(other) and not self.__gt__(other))

    def __le__(self, other: 'FormDataField'):
        """
        Determine if this object is less than or equal to another object.

        :param other: A FormDataField object to compare to.
        """

        return (self.__eq__(other) or not self.__gt__(other))
