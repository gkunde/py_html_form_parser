

def parse_int(value: str, default: int = None) -> int:
    """
    An integer parser for strings. Returning the parsed integer value or the
    provided default when parsing fails.

    Note: Value types that python can natively cast to integers will return
    the casted result. Example: True => 1

    :param val: string to parse integer from

    :param default: A value to return when parsing the string fails.
    """

    result = value
    if not isinstance(value, int):

        try:
            result = int(value)
        except ValueError:
            result = default

    return result


class FormFieldValue:
    """
    Form Field Value model, for storing the value of a form field input or
    control.

    :param value: The input field value

    :param is_selected: Determines if the value will be submitted with HTML
        form post.

    :param binary_path: A string representing a local file path to submit
        binary data with HTTP post.
    """

    BUTTON_TYPES = ("image", "reset", "search", "submit", )

    def __init__(self, value: str = None, is_selected: bool = True, binary_path: str = None):

        self.__data = {"value": None,
                       "is_selected": True,
                       "binary_path": None}

        self.value = value
        self.is_selected = is_selected
        self.binary_path = binary_path

    @property
    def value(self) -> str:
        return self.__data["value"]

    @value.setter
    def value(self, value: str):
        self.__data["value"] = value

    @property
    def binary_path(self) -> str:
        return self.__data["binary_path"]

    @binary_path.setter
    def binary_path(self, value: str):
        self.__data["binary_path"] = value

    @property
    def is_selected(self) -> bool:
        return self.__data["is_selected"]

    @is_selected.setter
    def is_selected(self, value: bool):
        self.__data["is_selected"] = value

    @classmethod
    def from_bs4(cls, bs4parser: 'bs4.BeautifulSoup') -> 'FormFieldValueModel':
        """
        Parses a BeautifulSoup object for a HTML form field's values. Also
        populates field values with defaults when no value is defined.

        :param bs4parser: A BeautifulSoup object containing the form field
        """

        value = {
            "value": cls.parse_input_value(bs4parser.name, bs4parser.get_text(), bs4parser.attrs),
            "is_selected": cls.parse_selected_status(bs4parser.name, bs4parser.attrs)
        }

        return cls.from_dict(value)

    @classmethod
    def from_dict(cls, value: dict) -> 'FormFieldValueModel':
        """
        Parses a dictionary object into a Form Field Value model object.

        :param value: A dictionary containing a HTML form field attributes
        """

        value_obj = FormFieldValue(value["value"], value["is_selected"])

        if "binary_path" in value:
            value_obj.binary_path = value["binary_path"]

        return value_obj

    def to_dict(self) -> dict:
        """
        Dumps the properties to a dictionary.
        """

        return self.__data

    @classmethod
    def parse_input_value(cls, tag_name: str, tag_text: str, tag_attrs: dict = {}) -> str:
        """
        The provided values and objects, obtains the value or determines a
        default for a form field.

        :param tag_name: The HTML form field tag/element name

        :param tag_text: The inline text for the element (not the contents of
            the value attribute)

        :param tag_attrs: Attributes from the HTML form field
        """

        result = tag_attrs.get("value", None)
        attr_type = tag_attrs.get("type", "").strip().lower()

        if result is None:

            if tag_name in ("button", "option", "textarea", ):
                # tags that store their value as "text" between the tags
                result = tag_text

            elif attr_type in ("checkbox", "radio", ):
                # default value for toggled inputs
                result = "on"

            elif attr_type == "color":
                # default value for GUI selectable inputs
                result = "#000000"

            elif attr_type == "range":
                # default value for slider based inputs

                attr_min = parse_int(tag_attrs.get("min", 0), 0)
                attr_max = parse_int(tag_attrs.get("max", 100), 100)

                if attr_max < attr_min:
                    result = str(attr_min)
                else:
                    # Integer division, seldom is float used with range
                    result = str(attr_min + (attr_max - attr_min) // 2)

            elif tag_name != "button" and attr_type in cls.BUTTON_TYPES:
                # controls with no value get default text
                # button controls always get empty string
                result = "Submit Query"

            else:
                # Do not assume value is an empty string, until we know the input type
                result = ""

        return result

    @classmethod
    def parse_selected_status(cls, tag_name: str, tag_attrs: dict = {}):
        """
        The provided values and objects obtain the selected status of a form
        field. The selected status determines a form fields inclusion during
        an HTTP post event.

        :param tag_name: The HTML form field tag/element name

        :param tag_attrs: Attributes from the HTML form field
        """

        # It is assumed a form field would normally be posted.
        result = True

        attr_type = tag_attrs.get("type", "").strip().lower()

        if tag_name == "button" or attr_type in cls.BUTTON_TYPES:
            # form controls always set to False, application must choose one
            # to include with form data.
            result = False

        elif tag_name == "option":
            result = "selected" in tag_attrs

        elif attr_type in ("checkbox", "radio", ):
            result = "checked" in tag_attrs
        
        return result

