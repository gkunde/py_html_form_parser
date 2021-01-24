

class FormElement:

    def __init__(self, name: str = None, value: str = None, binary_path: str = None, is_selected: str = None, primary_type: str = None, secondary_type: str = None):
        """
        """

        self.name = name
        self.value = value
        self.is_selected = is_selected
        self.binary_path = binary_path
        self.primary_type = primary_type
        self.secondary_type = secondary_type
