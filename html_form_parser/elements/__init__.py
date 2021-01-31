

class FormElement:
    """
    Represents a single form element.

    :param name: The name attribute of the element.

    :param value: The value attribute of the element.

    :param binary_path: For file upload element, a local filepath to be
        uploaded.

    :param is_selected: A flag to determine if the element

    :param tag_name: An element/tag's name

    :param type_attribute: The element's "type" attribute
    """

    def __init__(
            self,
            name: str = None,
            value: str = None,
            binary_path: str = None,
            is_selected: bool = None,
            tag_name: str = None,
            type_attribute: str = None):

        self._is_selected = None

        self.name = name
        self.value = value
        self.is_selected = is_selected
        self.binary_path = binary_path
        self.tag_name = tag_name
        self.type_attribute = type_attribute

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value):
        # ensure that is_selected has a true boolean value.
        self._is_selected = bool(value)

    def to_http_post(self):
        """
        """

        return (self.name, self.value, self.binary_path, )
