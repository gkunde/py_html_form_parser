

class FormElement:

    def __init__(
            self,
            name: str = None,
            value: str = None,
            binary_path: str = None,
            is_selected: bool = None,
            primary_type: str = None,
            secondary_type: str = None):

        self._is_selected = None

        self.name = name
        self.value = value
        self.is_selected = is_selected
        self.binary_path = binary_path
        self.primary_type = primary_type
        self.secondary_type = secondary_type

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value):
        self._is_selected = bool(value)
