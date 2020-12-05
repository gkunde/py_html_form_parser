import re
from typing import List

from .form_control import FormControl
from .form_field import FormField


class Form:
    """
    HTML Form model, for storing attributes of the form and its input fields.

    :param name: The name attribute of the form.

    :param id: The id attribute of the form.

    :param fields: A collection of FormFieldModel objects.
    """

    DEFAULT_ENCODING_TYPE = "application/x-www-form-urlencoded"
    DEFAULT_METHOD = "GET"
    DEFAULT_CHARSET = "utf-8"

    def __init__(self, name: str = None, id: str = None, fields: List[FormField] = None, controls: List[FormField] = None):

        self.__data = {
            "name": None,
            "id": None,
            "accepted_charset": self.DEFAULT_CHARSET,
            "encoding_type": self.DEFAULT_ENCODING_TYPE,
            "method": self.DEFAULT_METHOD,
            "fields": [],
            "controls": [],
        }

        self.__fields_key_index = {}
        self.__controls_key_index = {}

        self.name = name
        self.id = id

        if fields is not None:
            self.fields_add_range(fields)

        if controls is not None:
            self.controls_add_range(controls)

    def get_field_by_name(self, field_name: str) -> FormField:
        """
        Returns the first encountered field matching the name. Return value of
        None means no field was found.

        :param name: The name attribute of the field.
        """

        results = [field for field in self.fields if field.name == field_name][:1]

        if len(results) == 1:
            return results[0]

        return None

    def get_control_by_name(self, control_name) -> FormControl:
        """
        Returns the first encountered control matching the provided name.
        Return value of None means no field was found.

        :param name: The name attribute of the form control.
        """

        results = [control for control in self.controls if control.name == control_name][:1]

        if len(results) == 1:
            return results[0]

        return None

    @property
    def name(self):
        return self.__data["name"]

    @name.setter
    def name(self, value):
        self.__data["name"] = value

    @property
    def id(self):
        return self.__data["id"]

    @id.setter
    def id(self, value):
        self.__data["id"] = value

    @property
    def accepted_charset(self):
        return self.__data["accepted_charset"]

    @accepted_charset.setter
    def accepted_charset(self, value: str):
        self.__data["accepted_charset"] = value

    @property
    def encoding_type(self):
        return self.__data["encoding_type"]

    @encoding_type.setter
    def encoding_type(self, value: str):
        self.__data["encoding_type"] = value

    @property
    def method(self):
        return self.__data["method"]

    @method.setter
    def method(self, value: str):
        self.__data["method"] = value

    @property
    def fields(self):
        return self.__data["fields"]

    def fields_add_range(self, formfields: List[FormField]):
        """
        Extends fields property with the collection of FormFieldModels.
        """

        for formfield in formfields:
            self.fields_append(formfield)

    def fields_append(self, formfield: FormField):
        """
        Append a single FormFieldModel object to the fields collection.
        """

        field_key = "%s---%s" % (formfield._type, formfield.name, )
        field_key_idx = self.__fields_key_index.get(field_key, None)

        if field_key_idx is None:
            self.__fields_key_index[field_key] = len(self.fields)
            self.__data["fields"].append(formfield)

        else:
            self.__data["fields"][field_key_idx].values_add_range(formfield.values)

    @property
    def controls(self):
        return self.__data["controls"]

    def controls_add_range(self, controls: List[FormField]):
        """
        Extends controls property with the collection of FormFieldModels.
        """

        for control in controls:
            self.controls_append(control)

    def controls_append(self, value: FormField):
        """
        Append a single FormFieldModel object to the controls collection.
        """

        control_key = "%s---%s" % (value._type, value.name, )
        control_key_idx = self.__controls_key_index.get(control_key, None)

        if control_key_idx is None:
            self.__controls_key_index[control_key] = len(self.fields)
            self.__data["controls"].append(value)

        else:
            self.__data["controls"][control_key_idx].values_add_range(value.values)

    @classmethod
    def from_bs4(cls, bs4parser: 'bs4.BeautifulSoup', include_fields: bool = True, include_controls: bool = True) -> 'FormModel':
        """
        Capture and create a Form model from a BeautifulSoup object focused at
        a "form" HTML node.

        Note: To capture fields and controls, use the parser in the
        form_manager library.

        :param bs4parser: A BeautifulSoup object to capture from.

        :param include_fields: When true, form fields will be parsed into the
            object.

        :param include_controls: When true, form controls will be parsed into
            the object.
        """

        form_attrs = {
            "name": bs4parser.attrs.get("name", None),
            "id": bs4parser.attrs.get("id", None),
        }

        for option_attr in ("enctype", "method", ):

            if bs4parser.has_attr(option_attr):
                form_attrs[option_attr] = bs4parser.attrs[option_attr]

        if bs4parser.has_attr("accept-charset"):

            if isinstance(bs4parser.attrs["accept-charset"], list):
                form_attrs["accept-charset"] = bs4parser.attrs["accept-charset"][0]
            else:
                form_attrs["accept-charset"] = bs4parser.attrs["accept-charset"]

        form_obj = cls.from_dict(form_attrs, False, False)

        bs4_body = bs4parser.find_parent("body")

        if include_fields:

            fields = bs4parser.find_all(FormField.VALID_FIELDS, attrs={"form": False})
            if form_obj.id is not None and bs4_body is not None:
                # find any fields that may exist outside the form node.
                fields.extend(bs4_body.find_all(
                    FormField.VALID_FIELDS, attrs={"form": form_obj.id}))

            for field in fields:

                if field.attrs.get("type", "").strip().lower() in FormControl.VALID_CONTROL_TYPES:
                    continue

                form_field = FormField.from_bs4(field)

                form_obj.fields_append(form_field)

        if include_controls:

            regex_attr_types = re.compile(r"(%s)" % (
                "|".join(FormControl.VALID_CONTROL_TYPES)), re.I)

            controls = bs4parser.find_all(FormControl.VALID_CONTROLS,
                                          attrs={"type": regex_attr_types, "form": False})
            if form_obj.id is not None and bs4_body is not None:
                # find any controls that may exist outside the form node.
                controls.extend(bs4_body.find_all(FormControl.VALID_CONTROLS, attrs={
                                "form": form_obj.id, "type": regex_attr_types}))

            for control in controls:

                form_control = FormControl.from_bs4(control)

                form_obj.controls_append(form_control)

        return form_obj

    @classmethod
    def from_dict(cls, form: dict, include_fields: bool = True, include_controls: bool = True) -> 'FormModel':
        """
        Capture and create a form model from a dictionary.

        :param form: A dictionary containing the properties to be populated.
        """

        attr_name = form.get("name", None)
        attr_id = form.get("id", None)
        attr_enctype = form.get("enctype", cls.DEFAULT_ENCODING_TYPE)
        attr_method = form.get("method", cls.DEFAULT_METHOD)
        attr_accept_charset = form.get("accept-charset", cls.DEFAULT_CHARSET)

        form_obj = Form(attr_name, attr_id)
        form_obj.accepted_charset = attr_accept_charset
        form_obj.encoding_type = attr_enctype
        form_obj.method = attr_method

        if include_fields and "fields" in form:
            for field in form["fields"]:
                form_obj.fields_append(FormField.from_dict(field))

        if include_controls:
            for field in form["controls"]:
                form_obj.controls_append(FormField.from_dict(field))

        return form_obj

    def to_dict(self, include_fields: bool = True, include_controls: bool = True) -> dict:
        """
        Generate a dictionary object of the properties. Optional include
        fields and controls with parameters.

        :param include_fields: When true, the field collection is included.

        :param include_controls: When true. the control collection is
            included.
        """

        form = {
            "name": self.name,
            "id": self.id,
            "enctype": self.encoding_type,
            "method": self.method,
            "accept-charset": self.accepted_charset,
            "fields": [],
            "controls": []
        }

        if include_fields:
            form["fields"] = [field.to_dict() for field in self.fields]

        if include_controls:
            form["controls"] = [control.to_dict() for control in self.controls]

        return form

    def to_http_post(self) -> List[tuple]:
        """
        Generate a collection of tuples, suitable for use with an HTTP post
        request.
        """

        results = []
        for field in self.fields:
            for value in field.values:
                if value.is_selected:
                    results.append((field.name, value.value))

        for control in self.controls:
            for value in control.values:
                if control.is_selected:
                    results.append((control.name, value.value))

        return results
