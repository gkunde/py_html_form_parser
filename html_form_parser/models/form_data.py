from .form_data_field_collection import FormDataFieldCollection

class FormData:
    """
    An object for storing an HTML Form as a multipart/form-data type object.

    :param name: A name attributed to the form.

    :param action: The URL the form data is to be sent to.

    :param method: The HTTP verb type to use when sending the form data.

    :param enctype: The Form Data encoding type.
    """

    def __init__(self, name: str, action: str, method: str = "GET", enctype: str = "multipart/form-data"):

        self.name = name
        self.action = action.strip()
        self.method = method.strip().upper()
        self.enctype = enctype.strip()

        self.fields = FormDataFieldCollection()
