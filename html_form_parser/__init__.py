import re
from typing import List

from bs4 import BeautifulSoup

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

    :param html: A string containing HTML markup.

    :param name: Specific form to parse from the HTML, None will default to
        the first encountered form.
    """

    # form element types to skip when parsing
    __EXCLUDE_TYPES = ("reset", "search", )

    def __init__(self, html: str, name: str = None):

        self._attributes = {}
        self.__reset_attributes()

        self._fields = FormFieldCollection()

        if html is not None:
            self.__parse(html, name)

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

    def __parse(self, html: str, name: str = None):
        """
        Parse HTML markup for "form" element, optionally selecting "form"
        element by name.

        :param html: HTML markup

        :param name: Filter to select form by given name, else first form is
            returned.
        """

        bs4parser = BeautifulSoup(html, "html5lib")

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

        find_attrs = {}
        if name is not None:
            find_attrs["name"] = name

        form = bs4parser.find("form", attrs=find_attrs)

        if form is None:
            raise RuntimeError("no form found in markup")

        self.__reset_attributes()

        for name, value in form.attrs.items():
            self._attributes[name] = value

        element_attrs_filters = [{"form": False}]
        if form.attrs.get("id", None) is not None:
            element_attrs_filters.append({"form": form.attrs["id"]})

        for attr_filter in element_attrs_filters:

            for field in form.find_all(("button", "input", "select", "textarea", ), attrs=attr_filter):

                default_type = "text"
                if field.name == "button":
                    default_type = "submit"

                field_type = field.attrs.get("type", default_type).strip().lower()

                if field_type in self.__EXCLUDE_TYPES:
                    continue

                for parser in parsers:

                    if parser.suitable(field.name, field_type.strip().lower()):

                        self._fields.extend(parser.parse(field))

                        break

        return None

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
