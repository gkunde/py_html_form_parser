from typing import List

from bs4 import BeautifulSoup, Tag

from ..models.form_data_entry import FormDataEntry


class FormDataEntryParser:
    """
    A parser for HTML form elements.
    """

    # A series of class constants that can be overridden by derived classes.
    _default_name = None
    _default_value = None
    _default_type = None
    _default_is_selected = True

    __suitable_tags = ("button", "input", "select", "textarea", )

    def parse(self, html: str) -> List[FormDataEntry]:
        """
        Parse an HTML form element tag and generates a collection of form
        elements. A collection is returned as some elements such as "select"
        have multiple options.

        :param html: A string containing only the HTML tag, or a Beautiful
            Soup object of the tag.
        """

        bs4_parser = self._make_bs4_parser(html)

        attribute_name = self._get_name_attr(bs4_parser)
        attribute_value = self._get_value_attr(bs4_parser)
        attribute_selected = self._get_selected_state(bs4_parser)

        form_element = FormDataEntry(
            name=attribute_name,
            value=attribute_value,
            is_submitable=attribute_selected)

        return [form_element, ]

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        # This parser works for all form element types.
        return tag_name in self.__suitable_tags

    def _make_bs4_parser(self, html: str) -> 'bs4.Tag':
        """
        Creates a BeautifulSoup parser object for the given HTML fragment.
        Assumes if an HTML fragment is provided, the fragment is the desired
        tag to be parsed.
        """

        bs4_parser = html
        if not isinstance(html, (Tag, BeautifulSoup, )):
            # Only create a beautiful soup object if one isn't provided.
            bs4_parser = BeautifulSoup(html, "html5lib")

            # html5lib builds a full and valid DOM when parsing.
            bs4_parser = bs4_parser.body.next_element

        return bs4_parser

    def _get_value_attr(self, bs4_parser: 'bs4.Tag') -> str:
        """
        Returns the element's "value" attribute value. Defaults to class
        constant DEFAULT_VALUE when attribute is not defined.
        """

        return bs4_parser.attrs.get("value", self._default_value)

    def _get_name_attr(self, bs4_parser: 'bs4.Tag') -> str:
        """
        Returns the element's "name" attribute value. Defaults to class
        constant DEFAULT_NAME when attribute is not defined.
        """

        return bs4_parser.attrs.get("name", self._default_name)

    def _get_type_attr(self, bs4_parser: 'bs4.Tag') -> str:
        """
        Returns the element's "type" attrbute value. Defaults to class
        constant DEFAULT_TYPE when attribute is not defined.
        """

        return bs4_parser.attrs.get("type", self._default_type)

    def _get_selected_state(self, bs4_parser: 'bs4.Tag') -> bool:
        """
        Returns the elements "selected" status. Always returns true for
        unspecified form elements.
        """

        return self._default_is_selected

    def _get_tag_name(self, bs4_parser: 'bs4.Tag') -> str:
        """
        Returns the element's name/type
        """

        return bs4_parser.name


class ButtonFormElementParser(FormDataEntryParser):
    """
    A parser for HTML form button elements.
    """

    # Button default type is submit when undefined.
    _default_type = "submit"

    # Buttons require user activation to be "selected"
    _default_is_selected = False

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "button"


class InputFormElementParser(FormDataEntryParser):
    """
    A parser for HTML form input elements.
    """

    # Inputs without a defined type are defaulted to text
    _default_type = "text"

    # Inputs are defaulted to text, which implies the default value will be blank.
    _default_value = ""

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "input"


class SelectFormElementParser(FormDataEntryParser):

    _default_is_selected = False

    def parse(self, html: str) -> List[FormDataEntry]:
        """
        Overrides base class to present a select element and its options set
        as a collection of form elements. This parser treats the select
        options as if they were individual checkbox or radio input types.
        """

        bs4_parser = self._make_bs4_parser(html)

        elements = []

        for option in bs4_parser.find_all("option"):

            name = self._get_name_attr(bs4_parser)
            value = self._get_value_attr(option)
            is_selected = self._get_selected_state(option)

            elements.append(
                FormDataEntry(name=name,
                              value=value,
                              is_submitable=is_selected))

        return elements

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "select"

    def _get_selected_state(self, bs4_parser: 'bs4.Tag') -> bool:
        """
        Overrides base class to use element's "selected" attribute.
        """

        return bs4_parser.has_attr("selected")

    def _get_value_attr(self, bs4_parser: 'bs4.Tag') -> str:
        """
        Overrides base class to get element's "value" attribute or text value.
        """

        return bs4_parser.attrs.get("value", bs4_parser.get_text())


class TextareaFormElementParser(FormDataEntryParser):
    """
    Parser for HTML textarea elements.
    """

    _default_value = ""

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "textarea"

    def _get_value_attr(self, bs4_parser: 'bs4.Tag') -> str:
        """
        Overrides base classs to get the value from the element's
        .get_text() method.

        :param bs4_parser: A Beautiful Soup object, or object containing a get
        """

        return (bs4_parser.get_text() or self._default_value)


class SelectableInputFormElementParser(InputFormElementParser):
    """
    A parser for HTML form input elements of type "checkbox" or "radio"
    """

    _default_type = "checkbox"
    _default_value = "on"
    _default_is_selected = False

    __suitable_types = ("checkbox", "radio", )

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "input" and type_attribute in self.__suitable_types

    def _get_selected_state(self, bs4_parser: 'bs4.Tag') -> bool:
        """
        Overrides the base class to return the actual "checked" state of the
        element.
        """

        return bs4_parser.has_attr("checked")


class ColorInputFormElementParser(InputFormElementParser):
    """
    Parser for HTML input elements of type "color"
    """

    _default_type = "color"
    _default_value = "#000000"

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "input" and type_attribute == "color"


class RangeInputFormElementParser(InputFormElementParser):
    """
    Parser for HTML input elements of type "range"
    """

    _default_type = "range"

    __default_min_value = 0
    __default_max_value = 100

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "input" and type_attribute == "range"

    def _convert_str_to_int(self, value: str, default: int = None) -> int:
        """
        A convenience method for converting a string value to an integer and
        defining a default when the conversion fails.
        """

        try:
            return int(value)
        except:
            return default

    def _get_value_attr(self, bs4_parser: 'bs4.Tag') -> str:
        """
        Overrides the base class to return a generated default value when the
        value attribute is not defined.
        """

        value = bs4_parser.attrs.get("value", None)

        if value is None:

            attribute_min = self._convert_str_to_int(
                bs4_parser.attrs.get("min", self.__default_min_value), self.__default_min_value)

            attribute_max = self._convert_str_to_int(
                bs4_parser.attrs.get("max", self.__default_max_value), self.__default_max_value)

            if attribute_max < attribute_min:
                value = str(attribute_min)
            else:
                value = str(attribute_min + (attribute_max - attribute_min) // 2)

        return value


class SubmitInputFormElementParser(InputFormElementParser):
    """
    Parser for HTML input elements of type "submit"
    """

    _default_type = "submit"
    _default_value = "submit"
    _default_is_selected = False

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "input" and type_attribute == "submit"


class ButtonInputFormElementParser(SubmitInputFormElementParser):
    """
    Parser for HTML input elements of type "button" and "reset"
    """

    _default_type = "button"
    _default_value = None
    _default_is_selected = False

    __suitable_types = ("button", "reset", "search", )

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "input" and type_attribute in self.__suitable_types


class ImageInputFormElementParser(SubmitInputFormElementParser):
    """
    Parser for HTML input elements of type "image"
    """

    _default_type = "image"
    _default_value = "0"

    __name_attribute_suffixes = ("x", "y", )

    def parse(self, html: str) -> List[FormDataEntry]:
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
        for suffix in self.__name_attribute_suffixes:

            element_name = suffix
            if form_element.name is not None:
                element_name = "%s.%s" % (form_element.name, suffix, )

            form_elements.append(FormDataEntry(
                name=element_name,
                value=form_element.value,
                is_submitable=form_element.is_submitable))

        return form_elements

    def suitable(self, tag_name: str, type_attribute: str) -> bool:
        """
        Determine if the parser is appropriate for the given HTML element tag
        and type.

        :param tag_name: The HTML element name

        :param type_attribute: The HTML element "type" attribute. If no
            attribute is present, provide None.
        """

        return tag_name == "input" and type_attribute == "image"

    def _get_value_attr(self, bs4_parser: 'bs4.Tag') -> str:
        """
        Overrides InputFormElementParser to always return a value of "0". This
        element type indicates the coordinates where the image was clicked
        when submitted.
        """

        return self._default_value
