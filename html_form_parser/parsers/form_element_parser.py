from typing import List

from bs4 import BeautifulSoup, Tag

from ..elements import FormElement


class FormElementParser:
    """
    A parser for HTML form elements.
    """

    DEFAULT_NAME = None
    DEFAULT_VALUE = None
    DEFAULT_TYPE = None
    DEFAULT_IS_SELECTED = True

    def _make_bs4_parser(self, html: str) -> BeautifulSoup:
        """
        Creates a BeautifulSoup parser object for the given HTML fragment.
        Assumes if an HTML fragment is provided, the fragment is the targetted
        tag to be parsed.
        """

        bs4_parser = html
        if not isinstance(html, (Tag, BeautifulSoup, )):
            # Only create a beautiful soup object if one isn't provided.
            bs4_parser = BeautifulSoup(html, "html5lib")

            # html5lib builds a full and valid DOM when parsing.
            bs4_parser = bs4_parser.body.next_element

        return bs4_parser

    def _get_value_attr(self, bs4_parser: BeautifulSoup) -> str:
        """
        Returns the element's "value" attribute value. Defaults to None when
        attribute is not found.
        """

        return bs4_parser.attrs.get("value", self.DEFAULT_VALUE)

    def _get_name_attr(self, bs4_parser: BeautifulSoup) -> str:
        """
        Returns the element's "name" attribute value. Defaults to None when
        attribute is not found.
        """

        return bs4_parser.attrs.get("name", self.DEFAULT_NAME)

    def _get_type_attr(self, bs4_parser: BeautifulSoup) -> str:
        """
        """

        return bs4_parser.attrs.get("type", self.DEFAULT_TYPE)

    def _get_selected_state(self, bs4_parser: BeautifulSoup) -> bool:
        """
        Returns the elements "selected" status. Always returns true for
        unspecified form elements.
        """

        return self.DEFAULT_IS_SELECTED

    def _get_element_type(self, bs4_parser: BeautifulSoup) -> str:
        """
        Returns the element's name/type
        """

        return bs4_parser.name

    def parse(self, html: str) -> List[FormElement]:
        """
        """

        bs4_parser = self._make_bs4_parser(html)

        primary_type = self._get_element_type(bs4_parser)
        secondary_type = self._get_type_attr(bs4_parser)

        attribute_name = self._get_name_attr(bs4_parser)
        attribute_value = self._get_value_attr(bs4_parser)
        attribute_selected = self._get_selected_state(bs4_parser)
        attribute_binary_path = None

        return [FormElement(attribute_name, attribute_value, attribute_binary_path, attribute_selected, primary_type, secondary_type), ]


class ButtonFormElementParser(FormElementParser):
    """
    A parser for HTML form button elements.
    """

    # Button default type is submit when undefined.
    DEFAULT_TYPE = "submit"

    # Buttons require user activation to be "selected"
    DEFAULT_IS_SELECTED = False


class InputFormElementParser(FormElementParser):
    """
    A parser for HTML form input elements.
    """

    # Inputs without a defined type are defaulted to text
    DEFAULT_TYPE = "text"

    # Inputs are defaulted to text, which implies the default value will be blank.
    DEFAULT_VALUE = ""


class SelectFormElementParser(FormElementParser):

    DEFAULT_IS_SELECTED = False

    def _get_selected_state(self, bs4_parser: BeautifulSoup) -> bool:
        """
        Overrides base class to use element's "selected" attribute.
        """

        return bs4_parser.has_attr("selected")

    def _get_value_attr(self, bs4_parser: BeautifulSoup) -> str:
        """
        Overrides base class to get element's "value" attribute or text value.
        """

        return bs4_parser.attrs.get("value", bs4_parser.get_text())

    def parse(self, html: str) -> List[FormElement]:
        """
        Overrides base class to present a select element and its options set
        as a collection of form elements. This parser treats the select
        options as if they were individual checkbox or radio input types.
        """

        bs4_parser = self._make_bs4_parser(html)

        elements = []

        for option in bs4_parser.find_all("option"):

            primary_type = bs4_parser.name
            secondary_type = self.DEFAULT_TYPE
            name = self._get_name_attr(bs4_parser)
            value = self._get_value_attr(option)
            is_selected = self._get_selected_state(option)
            binary_path = None

            elements.append(
                FormElement(name,
                            value,
                            binary_path,
                            is_selected,
                            primary_type,
                            secondary_type))

        return elements


class TextareaFormElementParser(FormElementParser):
    """
    Parser for HTML textarea elements.
    """

    DEFAULT_VALUE = ""

    def _get_value_attr(self, bs4_parser: BeautifulSoup) -> str:
        """
        Overrides FormElementParser, to get the value from the element's
        .get_text() method.
        """

        return (bs4_parser.get_text() or self.DEFAULT_VALUE)


class CheckboxInputFormElementParser(InputFormElementParser):
    """
    A parser for HTML form input elements of type "checkbox" or "radio"
    """

    DEFAULT_TYPE = "checkbox"
    DEFAULT_VALUE = "on"
    DEFAULT_IS_SELECTED = False

    def _get_selected_state(self, bs4_parser: BeautifulSoup) -> bool:
        """
        Overrides the base class to return the actual "checked" state of the
        element.
        """

        return bs4_parser.has_attr("checked")


class ColorInputFormElementParser(InputFormElementParser):
    """
    Parser for HTML input elements of type "color"
    """

    DEFAULT_TYPE = "color"
    DEFAULT_VALUE = "#000000"


class RadioInputFormElementParser(CheckboxInputFormElementParser):
    """
    A parser for HTML form input elements of type "checkbox" or "radio"
    """
    # This has the same functionality as a checkbox
    DEFAULT_TYPE = "radio"


class RangeInputFormElementParser(InputFormElementParser):
    """
    Parser for HTML input elements of type "range"
    """

    DEFAULT_TYPE = "range"
    DEFAULT_MIN_VALUE = 0
    DEFAULT_MAX_VALUE = 100

    def _convert_str_to_int(self, value: str, default: int = None) -> int:
        """
        A convenience method for converting a string value to an integer and
        defining a default when the conversion fails.
        """

        try:
            return int(value)
        except:
            return default

    def _get_value_attr(self, bs4_parser: BeautifulSoup) -> str:
        """
        Overrides the base class to return a generated default value when the
        value attribute is not defined.
        """

        value = bs4_parser.attrs.get("value", None)

        if value is None:

            attribute_min = self._convert_str_to_int(
                bs4_parser.attrs.get("min", self.DEFAULT_MIN_VALUE), self.DEFAULT_MIN_VALUE)

            attribute_max = self._convert_str_to_int(
                bs4_parser.attrs.get("max", self.DEFAULT_MAX_VALUE), self.DEFAULT_MAX_VALUE)

            if attribute_max < attribute_min:
                value = str(attribute_min)
            else:
                value = str(attribute_min + (attribute_max - attribute_min) // 2)

        return value


class SubmitInputFormElementParser(InputFormElementParser):
    """
    Parser for HTML input elements of type "submit"
    """

    DEFAULT_TYPE = "submit"
    DEFAULT_VALUE = "submit"
    DEFAULT_IS_SELECTED = False


class ButtonInputFormElementParser(SubmitInputFormElementParser):
    """
    Parser for HTML input elements of type "button"
    """

    DEFAULT_TYPE = "button"
    DEFAULT_VALUE = None
    DEFAULT_IS_SELECTED = False


class ImageInputFormElementParser(SubmitInputFormElementParser):
    """
    Parser for HTML input elements of type "image"
    """

    DEFAULT_VALUE = "0"
    NAME_ATTR_SUFFIXES = ("x", "y", )

    def _get_value_attr(self, bs4_parser: BeautifulSoup) -> str:
        """
        Overrides InputFormElementParser to always return a value of "0". This
        element type indicates the coordinates where the image was clicked
        when submitted.
        """

        return self.DEFAULT_VALUE

    def parse(self, html: str) -> List[FormElement]:
        """
        Overrides base class to return two FormElement objects. As this input
        element type provides an coordinate that indicates where a user has
        clicked on the image.
        """

        # The only difference for this element and other input elements is
        # there are two fields generated for x, y coordinates. Use the base
        # class parse, then clone them into two separate FormElement objects.

        form_element = super().parse(html)[0]

        form_elements = []
        for suffix in self.NAME_ATTR_SUFFIXES:

            element_name = suffix
            if form_element.name is not None:
                element_name = "%s.%s" % (form_element.name, suffix, )

            form_elements.append(FormElement(
                name=element_name,
                value=form_element.value,
                binary_path=form_element.binary_path,
                is_selected=form_element.is_selected,
                primary_type=form_element.primary_type,
                secondary_type=form_element.secondary_type
            ))

        return form_elements


class ResetInputFormElementParser(SubmitInputFormElementParser):
    """
    Parser for HTML input elements of type "reset"
    """

    DEFAULT_TYPE = "reset"
    DEFAULT_IS_SELECTED = False
