import re
from typing import List

from bs4 import BeautifulSoup

from .form import Form


class FormManager:
    """
    A manager for parsing forms from an HTML source into Form data models.
    Parses the entire document for all HTML forms and creates Form model
    objects.

    :param html: A string containing HTML markup.
    """

    def __init__(self, html: str = None):

        self.forms = self.parse_forms(html)

        self.__form_id_index = {}
        self.__form_name_index = {}

        for index, form in enumerate(self.forms):

            if form.name is not None and form.name not in self.__form_name_index:
                self.__form_name_index[form.name] = index

            if form.id is not None and form.id not in self.__form_id_index:
                self.__form_id_index[form.id] = index

    def get_form_by_id(self, form_id):
        """
        Return a form identified by the ID attribute.

        Note: Only the first encountered form matching the ID is returned.

        :param form_id: The HTML form id attribute
        """

        index = self.__form_id_index.get(form_id, None)

        if index is None:
            raise IndexError("Form ID \"%s\", not found" % (form_id, ))

        return self.forms[index]

    def get_form_by_name(self, form_name):
        """
        Return a form identified by the name attribute.

        Note: Only the first encountered form matching the name is returned.

        :param form_name: The HTML form name attribute.
        """

        index = self.__form_name_index.get(form_name, None)

        if index is None:
            raise IndexError("Form name \"%s\", not found" % (form_name, ))

        return self.forms[index]

    @classmethod
    def parse_forms(cls, html: str) -> List[Form]:
        """
        Parser of HTML into a collection of Form objects

        :param html: A string containing HTML markup.
        """

        form_objects = []

        bs4parser = BeautifulSoup(html, "html5lib")

        for form in bs4parser.find_all("form"):
            form_objects.append(Form.from_bs4(form))

        return form_objects
