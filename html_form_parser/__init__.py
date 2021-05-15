import re
from typing import List

from bs4 import BeautifulSoup, Tag

from html_form_parser.models.form_data import FormData
from html_form_parser.models.form_data_entry import FormDataEntry
from html_form_parser.parsers import form_data_entry_parser


class HtmlFormParser:
    """
    Parse and extract HTML forms from a HTML page.
    """

    def __init__(self, markup: str = None, parser: str = None):
        """
        :param markup: A string containing HTML markup.

        :param parser: A string containing a valid BeautifulSoup parsing library name.
        """

        self.forms = []

        if markup is not None:
            self.parse(markup, parser)

    def parse(self, markup: str, parser: str = None) -> List[FormData]:
        """
        Convert a HTML page into Form Data objects

        :param markup: A string containing HTML markup.

        :param parser: A string property to select a BeutifulSoup Parser.

        :returns: A collection of ForData objects. The same objects are
            stored within the object.
        """

        if parser is None:
            parser = "html5lib"

        parsers = [
            form_data_entry_parser.SelectableInputFormElementParser(),
            form_data_entry_parser.ColorInputFormElementParser(),
            form_data_entry_parser.RangeInputFormElementParser(),
            form_data_entry_parser.SubmitInputFormElementParser(),
            form_data_entry_parser.ButtonInputFormElementParser(),
            form_data_entry_parser.ImageInputFormElementParser(),
            form_data_entry_parser.ButtonFormElementParser(),
            form_data_entry_parser.InputFormElementParser(),
            form_data_entry_parser.SelectFormElementParser(),
            form_data_entry_parser.TextareaFormElementParser(),
            form_data_entry_parser.FormDataEntryParser(),
        ]

        bs4_parser = BeautifulSoup(markup, parser)

        parsed_forms = bs4_parser.find_all("form")

        parsed_fields = bs4_parser.find_all(("button", "input", "select", "textarea", ))

        form_id_map = {}
        for index, parsed_form in enumerate(parsed_forms):

            if "id" in parsed_form.attrs:
                form_id_map[parsed_form.attrs["id"]] = index

            self.forms.append(self._create_form_data(parsed_form))

        # Fields associate to the nearest containing form node, or specify their form owner by attribute.
        # https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#association-of-controls-and-forms
        for parsed_field in parsed_fields:

            form_index = None
            if "form" in parsed_field.attrs:
                form_index = form_id_map.get(parsed_field.attrs["form"], None)

            if form_index is None:

                parent_form = parsed_field.find_parent("form")
                if parent_form is not None:
                    form_index = parsed_forms.index(parsed_form)

            if form_index is not None:
                self.forms[form_index].fields.extend(
                    self._create_form_data_field(parsed_field, parsers))

        return self.forms

    def _create_form_data(self, parsed_form: Tag) -> FormData:
        """
        Create Form Data from parsed form node object.

        :param parsed_form: A BeautifulSoup object containing a form.

        :returns: A FormData object
        """

        form_data = FormData()

        for key, val in parsed_form.attrs.items():

            match_key = key.lower()

            if match_key == "name":
                form_data.name = val

            elif match_key == "action":
                form_data.action = val.strip()

            elif match_key == "method":
                form_data.method = val.strip().upper()

            elif match_key == "enctype":
                form_data.enctype = val.strip()

        return form_data

    def _create_form_data_field(self, parsed_form_field: Tag, field_parsers: List[form_data_entry_parser.InputFormElementParser] = None) -> List[FormDataEntry]:
        """
        Create Form Data Entries from pasred form input element.

        :param parsed_form_field: A BeautifulSoup object containing an input field.

        :param field_parsers: A collection of HTML input element parsers.

        :returns: A collection of Form Data Entry objects
        """

        field_type = parsed_form_field.attrs.get("type", None)

        for parser in field_parsers:

            if field_type is not None and parser.suitable(parsed_form_field.name, field_type.strip().lower()):
                return parser.parse(parsed_form_field)

            elif parser.suitable(parsed_form_field.name, None):
                return parser.parse(parsed_form_field)

        return []
