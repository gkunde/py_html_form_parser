import copy
from typing import List


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
        except TypeError:
            result = default
        except ValueError:
            result = default

    return result


class FormField:
    """
    HTML Form Field, storing form field attributes and their values.

    :param name: Input field name attribute

    :param value: The value of the form input

    :param is_selected: A boolean to indicate if the field would be included
        when submitting the webform.

    :param binary_filepath: For "file" form types, this is the file path of
        the file to submit.
    """

    _SELECTABLE_INPUTS = ("checkbox", "radio", )
    _BUTTON_TYPES = ("image", "reset", "search", "submit", )
    _IGNORED_TYPES = ("reset", "search", )
    VALID_FIELDS = ("button", "input", "select", "textarea", )
    DEFAULT_INPUT_TYPE = "text"
    DEFAULT_BUTTON_TYPE = "submit"

    def __init__(self,
                 name: str = None,
                 value: str = None,
                 is_selected: bool = True,
                 binary_filepath: str = None):

        self._binary_path = None
        self._name = None
        self._is_selected = None
        self._value = None

        self.binary_path = binary_filepath
        self.is_selected = is_selected
        self.name = name
        self.value = value

    @property
    def binary_path(self):
        return self._binary_path

    @binary_path.setter
    def binary_path(self, value: str):
        self._binary_path = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if value is None:
            raise ValueError("name must not be None")
        self._name = str(value)

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value):
        self._is_selected = value == True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):

        if value is None:
            value = ""

        self._value = str(value)

    @classmethod
    def from_bs4(cls, bs4parser: 'bs4.BeautifulSoup') -> 'List[FormField]':
        """
        Parses a BeautifulSoup object for a HTML form field's attributes.

        :param bs4parser: A BeautifulSoup object containing the form field

        :returns: A collection of FormFields. A collection is returned as some
            input fields generate multiple fields such as "<select />"
            elements.
        """

        results = []

        tag = bs4parser.name
        tag_type = bs4parser.attrs.get("type", cls.DEFAULT_INPUT_TYPE).lower()

        if tag not in cls.VALID_FIELDS:
            raise ValueError("Invalid HTML tag: '%s'" % (tag, ))

        if tag == "button":
            tag_type = bs4parser.attrs.get("type", "submit").lower()

        if tag_type in cls._IGNORED_TYPES:
            # these types are never submitted with form fields
            return results

        name = bs4parser.attrs.get("name", None)
        value = bs4parser.attrs.get("value", None)
        is_selected = True
        binary_path = None

        if tag == "select":

            for option in bs4parser.find_all("option"):

                value = option.get("value", option.get_text())

                results.append(cls(name, value, option.has_attr("selected"), None))

        else:

            # Determine "is_selected" flag status
            if tag_type in cls._SELECTABLE_INPUTS:
                # input allows "flagging"

                is_selected = bs4parser.has_attr("checked")

            elif tag_type == "submit":
                # buttons are selected when "clicked"
                is_selected = False

            if tag == "textarea":
                value = bs4parser.get_text()

            # Determine a default value
            if value is None:

                if tag == "button":

                    value = bs4parser.get_text()
                    if value is None or value == "":
                        value = "Submit Query"

                if tag_type in cls._SELECTABLE_INPUTS:
                    value = "on"

                elif tag_type == "color":
                    value = "#000000"

                elif tag_type == "range":

                    range_max = parse_int(bs4parser.attrs.get("max", 100), 100)
                    range_min = parse_int(bs4parser.attrs.get("min", 0), 0)

                    if range_max < range_min:
                        value = str(range_min)
                    else:
                        value = str(range_min + (range_max - range_min) // 2)

            if value is None:
                value = ""

            if tag_type == "image":

                if name is None:
                    name = ""
                else:
                    name = name + "."

                results.append(cls(name + "x", "1", False, None))
                results.append(cls(name + "y", "1", False, None))

            elif name is not None:
                results.append(cls(name, value, is_selected, binary_path))

        return results

    @classmethod
    def from_dict(cls, value: dict) -> 'FormField':
        """
        Generate a FormField object from a dictionary

        Required dictionary keys are: name, value, is_selected, binary_path
        """
        return cls(value["name"], value["value"], value["is_selected"], value["binary_path"])

    def to_dict(self) -> dict:
        """
        Converts the contents of the FormField object to a dictionary.
        """
        return {"name": self.name, "value": self.value, "is_selected": self.is_selected, "binary_path": self.binary_path}

    def __dict__(self):
        """
        Calls on .to_dict()
        """
        return self.to_dict()

    def __eq__(self, compare_to: 'FormField') -> bool:
        """
        Evaluate properties to determine equality.
        """

        if self.name != compare_to.name:
            return False
        if self.value != compare_to.value:
            return False
        if self.is_selected != compare_to.is_selected:
            return False
        if self.binary_path != compare_to.binary_path:
            return False

        return True

    def __lt__(self, compare_to: 'FormField') -> bool:
        """
        Evaluate properties, in order of importance, to determine inequality
        of less than.
        """

        if self == compare_to:
            return False

        if self.name < compare_to.name:
            return True

        # Choosing not to evaluate the property "value" if either is None.
        if self.value is not None \
                and compare_to.value is not None \
                and self.value < compare_to.value:
            return True

        # Choosing not to evaluate the property "binary_path" if either
        # is None.
        if self.binary_path is not None \
                and compare_to.value is not None \
                and self.binary_path < compare_to.binary_path:
            return True

        if self.is_selected < compare_to.is_selected:
            return True

        return False

    def __gt__(self, compare_to: 'FormField') -> bool:
        """
        Evaluate properties, in order of importance, to determine inequality
        of greater than.
        """

        if self == compare_to:
            return False

        if self.name > compare_to.name:
            return True

        # Choosing not to evaluate the property "value" if either is None.
        if self.value is not None \
                and compare_to.value is not None \
                and self.value > compare_to.value:
            return True

        # Choosing not to evaluate the property "binary_path" if either
        # is None.
        if self.binary_path is not None \
                and compare_to.binary_path is not None \
                and self.binary_path > compare_to.binary_path:
            return True

        if self.is_selected > compare_to.is_selected:
            return True

        return False

    def __le__(self, compare_to: 'FormField') -> bool:
        """
        Evaluate properties, in order of importance, to determine equality or
        less than.
        """

        if self == compare_to:
            return True

        return self < compare_to

    def __ge__(self, compare_to: 'FormField') -> bool:
        """
        Evaluate properties, in order of importance, to determine equality or
        greater than.
        """

        if self == compare_to:
            return True

        return self > compare_to

    def __ne__(self, compare_to: 'FormField') -> bool:
        """
        Evaluate properties to determine inequality.
        """
        return not (self == compare_to)
