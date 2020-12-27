import re
from typing import List

from .form_field import FormField
from .form_field_collection import FormFieldCollection


class Form:
    """
    HTML Form model, for storing attributes of the form and its input fields.

    :param name: The name attribute of the form.

    :param id: The id attribute of the form.

    :param action: The action attribute of the form.

    :param fields: A collection of FormFieldModel objects.
    """

    DEFAULT_ENCODING_TYPE = "application/x-www-form-urlencoded"
    DEFAULT_METHOD = "GET"
    DEFAULT_CHARSET = "utf-8"

    def __init__(self, name: str = None, id: str = None, action: str = None, fields: List[FormField] = None):

        self._name = None
        self._id = None
        self._action = None
        self._accepted_charset = self.DEFAULT_CHARSET
        self._encoding_type = self.DEFAULT_ENCODING_TYPE
        self._method = self.DEFAULT_METHOD
        self._fields = FormFieldCollection(fields)

        self.name = name
        self.id = id
        self.action = action

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value: str):
        self._action = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def accepted_charset(self):
        return self._accepted_charset

    @accepted_charset.setter
    def accepted_charset(self, value: str):
        self._accepted_charset = value

    @property
    def encoding_type(self):
        return self._encoding_type

    @encoding_type.setter
    def encoding_type(self, value: str):
        self._encoding_type = value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value: str):
        self._method = value

    @property
    def fields(self):
        return self._fields

    @classmethod
    def from_bs4(cls, bs4parser: 'bs4.BeautifulSoup', include_fields: bool = True) -> 'FormModel':
        """
        Capture and create a Form model from a BeautifulSoup object focused at
        a "form" HTML node.

        Note: To capture fields and controls, use the parser in the
        form_manager library.

        :param bs4parser: A BeautifulSoup object to capture from.

        :param include_fields: When true, form fields will be parsed into the
            object.
        """

        form_obj = cls(
            bs4parser.attrs.get("name", None),
            bs4parser.attrs.get("id", None),
            bs4parser.attrs.get("action", None)
        )

        form_obj.encoding_type = bs4parser.attrs.get("enctype", cls.DEFAULT_ENCODING_TYPE)
        form_obj.method = bs4parser.attrs.get("method", cls.DEFAULT_METHOD)

        if bs4parser.has_attr("accept-charset"):

            if isinstance(bs4parser.attrs["accept-charset"], list):
                form_obj.accepted_charset = bs4parser.attrs["accept-charset"][0]
            else:
                form_obj.accepted_charset = bs4parser.attrs["accept-charset"]

        bs4_body = bs4parser.find_parent("body")

        if include_fields:

            fields = bs4parser.find_all(FormField.VALID_FIELDS, attrs={"form": False})
            if form_obj.id is not None and bs4_body is not None:
                # find any fields that may exist outside the form node.
                fields.extend(bs4_body.find_all(
                    FormField.VALID_FIELDS, attrs={"form": form_obj.id}))

            for field in fields:

                form_field = FormField.from_bs4(field)

                form_obj.fields.extend(form_field)

        return form_obj

    @classmethod
    def from_dict(cls, form: dict, include_fields: bool = True) -> 'FormModel':
        """
        Capture and create a form model from a dictionary.

        :param form: A dictionary containing the properties to be populated.
        """

        attr_name = form.get("name", None)
        attr_id = form.get("id", None)
        attr_action = form.get("action", None)
        attr_enctype = form.get("enctype", cls.DEFAULT_ENCODING_TYPE)
        attr_method = form.get("method", cls.DEFAULT_METHOD)
        attr_accept_charset = form.get("accept-charset", cls.DEFAULT_CHARSET)

        form_obj = Form(attr_name, attr_id, attr_action)
        form_obj.accepted_charset = attr_accept_charset
        form_obj.encoding_type = attr_enctype
        form_obj.method = attr_method

        if include_fields and "fields" in form:
            for field in form["fields"]:
                form_obj.fields.append(FormField.from_dict(field))

        return form_obj

    def to_dict(self, include_fields: bool = True) -> dict:
        """
        Generate a dictionary object of the properties. Optional include
        fields and controls with parameters.

        :param include_fields: When true, the field collection is included.
        """

        form = {
            "name": self.name,
            "id": self.id,
            "action": self.action,
            "enctype": self.encoding_type,
            "method": self.method,
            "accept-charset": self.accepted_charset,
            "fields": []
        }

        if include_fields:
            form["fields"] = [field.to_dict() for field in self.fields]

        return form
