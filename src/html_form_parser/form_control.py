import copy
from typing import List

from .form_field_value import FormFieldValue


class FormControl:
    """
    HTML form control, storing attributes and values of a form control.

    :param name: Input field name attribute

    :param field_type: Input field type

    :param values: A collection of form field value models.
    """

    VALID_CONTROLS = ("button", "input", )
    VALID_CONTROL_TYPES = ("image", "submit", "search", "reset", )
    ACCEPTED_CONTROL_TYPES = ("image", "submit", )
    DEFAULT_INPUT_TYPE = "submit"

    def __init__(self, name: str = None, values: List[FormFieldValue] = None):

        self.__data = {"name": None,
                       "type": self.DEFAULT_INPUT_TYPE,
                       "values": []}

        self.name = name

        if values is not None:
            self.values_add_range(values)

    def set_control_selected_status(self, value: str, status: bool):
        """
        Set the is_selected property of a control's value

        :param value: The value to match on a value property
        """

        if not isinstance(status, bool):
            raise TypeError("Status must be of type boolean")

        results = [control_value for control_value in self.values if control_value.value == value]

        for result in results:
            result.is_selected = status

    @property
    def name(self) -> str:
        return self.__data["name"]

    @name.setter
    def name(self, val: str):
        self.__data["name"] = val

    @property
    def _type(self) -> str:
        return self.__data["type"]

    @_type.setter
    def _type(self, val: str):

        if val is not None:
            self.__data["type"] = val.strip().lower()

    @property
    def values(self) -> List[FormFieldValue]:
        return self.__data["values"]

    def values_add_range(self, values: List[FormFieldValue]):
        """
        Extends values property with the collection of FormFieldValueModel.
        """

        self.__data["values"].extend(values)

    def values_append(self, value: FormFieldValue):
        """
        Append a single FormFieldValueModel object to the values collection.
        """

        self.__data["values"].append(value)

    @classmethod
    def from_bs4(cls, bs4parser: 'bs4.BeautifulSoup') -> 'FormFieldModel':
        """
        Parses a BeautifulSoup object for a HTML form field's attributes.

        :param bs4parser: A BeautifulSoup object containing the form field
        """

        if bs4parser.name not in cls.VALID_CONTROLS:
            raise ValueError("Expected html form control, received: \"%s\"" % (bs4parser.name, ))

        attr_type = bs4parser.attrs.get("type", cls.DEFAULT_INPUT_TYPE).strip().lower()

        if attr_type not in cls.ACCEPTED_CONTROL_TYPES:
            raise ValueError("Unsupported html form control type: \"%s\"" % (attr_type, ))

        control = {
            "name": bs4parser.attrs.get("name", None),
            "type": attr_type,
            "values": []
        }

        control_obj = cls.from_dict(control)

        if attr_type == "image":
            # image "submit" types present an x,y cordinate where the user clicked.
            # Add two values for the x and y

            control_obj.values_append(FormFieldValue(1, False))
            control_obj.values_append(FormFieldValue(1, False))

        else:
            control_obj.values_append(FormFieldValue.from_bs4(bs4parser))

        return control_obj

    @classmethod
    def from_dict(cls, field: dict) -> 'FormFieldModel':
        """
        Parses a dictionary object into a Form Field model object.

        :param value: A dictionary containing a HTML form field attributes
        """

        values = [FormFieldValue.from_dict(field) for field in field["values"]]

        control_obj = FormControl(field["name"], values)

        if "type" in field and field["type"] != "":
            control_obj._type = field["type"]

        return control_obj

    def to_dict(self):
        """
        Dumps the properties to a dictionary
        """

        control = {
            "name": self.name,
            "type": self._type,
            "values": [val.to_dict() for val in self.values]
        }

        return control
