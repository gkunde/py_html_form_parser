import re
from typing import List, Iterator

from bs4 import BeautifulSoup, Tag

from .elements import FormElement
from .form_field_collection import FormFieldCollection
from .parsers import form_element_parser


class Form:
    """
    Creates a HTML form instance providing access to form attributes and form
    fields contained within the form. The first encountered form is parsed by
    default, while providing a name will search for a form of that name to be
    parsed instead.

    Primary attributes are provided as readonly properties, access to
    non-essential form attributes are available in the _attributes property.

    Form field elements are parsed into a collection provided by the fields
    property. Note, form controls buttons for "reset" and "search" are not
    captured.

    :param html: A string containing HTML markup, or a BeautifulSoup
        compatible object.

    :param index: When more than one form is available, select form by zero
        based index.
    """

    # form element types to skip when parsing
    __EXCLUDE_TYPES = ("reset", "search", )

    def __init__(self, html: str, index: int = 0):

        self._attributes = {}
        self.__reset_attributes()

        self._fields = FormFieldCollection()

        if html is not None:
            self.__parse(html, index)

    @property
    def name(self) -> str:
        return self._attributes["name"]

    @property
    def action(self) -> str:
        return self._attributes["action"]

    @property
    def method(self) -> str:
        return self._attributes["method"]

    @property
    def enctype(self) -> str:
        return self._attributes["enctype"]

    @property
    def fields(self) -> FormFieldCollection:
        return self._fields

    def __parse(self, html: str, index: int = 0):
        """
        Parse HTML markup for "form" element, optionally selecting "form"
        element by name.

        :param html: HTML markup

        :param name: Filter to select form by given name, else first form is
            returned.
        """

        html_soup = html
        if not isinstance(html_soup, (Tag, BeautifulSoup, )):
            html_soup = BeautifulSoup(html, "html5lib")

        # A collection of parsers. The order does matter, parsers earlier in
        # the list are more specific than parsers at the end.
        parsers = [
            form_element_parser.SelectableInputFormElementParser(),
            form_element_parser.ColorInputFormElementParser(),
            form_element_parser.RangeInputFormElementParser(),
            form_element_parser.SubmitInputFormElementParser(),
            form_element_parser.ButtonInputFormElementParser(),
            form_element_parser.ImageInputFormElementParser(),
            form_element_parser.ButtonFormElementParser(),
            form_element_parser.InputFormElementParser(),
            form_element_parser.SelectFormElementParser(),
            form_element_parser.TextareaFormElementParser(),
            form_element_parser.FormElementParser(),
        ]

        form_nodes = html_soup.find_all("form")

        if form_nodes is None or len(form_nodes) == 0:
            raise RuntimeError("no form found in markup")
        
        form_node = form_nodes[index]

        self.__reset_attributes()

        for name, value in form_node.attrs.items():
            self._attributes[name] = value

        for input_tag in self._find_all_input_tags(form_node, None):
            self._fields.extend(self._parse_input_tag(input_tag, parsers))

        if form_node.attrs.get("id", None) is not None:
            # Form's with an "id" attribute can enable fields to be placed
            # outside the "form" tag node.

            for input_tag in self._find_all_input_tags(html_soup, form_node.attrs["id"]):
                self._fields.extend(self._parse_input_tag(input_tag, parsers))

    def _find_all_input_tags(self, form_tag: 'bs4.Tag', form_id: str = None) -> 'Iterator[bs4.Tag]':
        """
        Yields all input field child tags from provided form_tag.

        :param form_tag: A html tag to fetch input tags from.

        :param form_id: When not None, returns all input tags with a matching
            value in their "form" attribute.
        """

        attrs = {"form": False}
        if form_id is not None:
            attrs = {"form": form_id}

        for input_tag in form_tag.find_all(("button", "input", "select", "textarea", ), attrs=attrs):
            yield input_tag

    def _parse_input_tag(self, input_tag: 'bs4.Tag', parsers: List[form_element_parser.FormElementParser]) -> List[FormElement]:
        """
        Returns a collection of FormElement objects from the given input_tag.

        :param input_tag: The form input tag to parse into FormElements

        :param parsers: A collection of parsers to be used for identifying and
            parsing the provided input_tag.
        """

        elements = []

        field_type = input_tag.attrs.get("type", "").strip().lower()

        for parser in parsers:

            if parser.suitable(input_tag.name, field_type):
                elements = parser.parse(input_tag)
                break

        return elements

    def __reset_attributes(self) -> None:
        """
        Reset the _attributes collection to default values.
        """

        self._attributes = {
            "name": None,
            "action": None,
            "method": None,
            "enctype": None
        }

    @classmethod
    def parse_by_name(cls, html: str, form_name: str) -> 'Form':
        """
        Finds and returns a Form with a matching name attribute.

        :param html: HTML markup string to parse

        :param form_name: A value to match a form's name attribute to.
        """

        parser = BeautifulSoup(html, "html5lib")

        index = None
        for idx, form in enumerate(parser.find_all("form")):

            if form.attrs.get("name", None) == form_name:

                index = idx

                break

        return cls(parser, index)

    @classmethod
    def parse_by_id_attribute(cls, html: str, form_id: str) -> 'Form':
        """
        Finds and returns a Form with a matching id attribute.

        :param html: HTML markup string to parse.

        :param form_id: A value to match a form's id attribute to.
        """

        parser = BeautifulSoup(html, "html5lib")

        index = None
        for idx, form in enumerate(parser.find_all("form")):

            if form.attrs.get("id", None) == form_id:

                index = idx

                break

        return cls(parser, index)
