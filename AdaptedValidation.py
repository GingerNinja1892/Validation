"""
Validates data according to characteristics describing the allowed data
"""

def my_round(x, n):
    return round(x, n) if n != 0 else round(x)

class Data:
    """
    Parent class of all data to hold characteristics so it can be verified that new data of that form abides by these parameters

    PARAMETERS:
    - type_ (type): The python type the data must be
    - allow_na (bool): Whether or not to allow an empty value
    """

    def __init__(self, type_, range_ = None, allow_na = False):

        self.type = type_
        self.range = range_
        self.allow_na = allow_na

class IntRange(Data):
    """
    Hold characteristics of integer data in a range

    PARAMETERS:
    - min_ (int): The minimum value the data can be, inclusive, defaults to None (no minimum)
    - max_ (int): The maximum value the data can be, inclusive, defaults to None (no maximum)
    - round_digits (int/None): The number of digits to round data to before checking (None if don't round)
    """

    def __init__(self, min_ = None, max_ = None, round_digits = None, allow_na = False):

        super().__init__(int, True, allow_na)
        self.min = min_
        self.max = max_
        self.round_digits = round_digits

class IntList(Data):
    """
    Hold characteristics of integer data that can take any value from a list

    PARAMETERS:
    - allowed (list): A list of allowed values data can be
    - round_digits (int/None): The number of digits to round data to before checking (None if don't round)
    """

    def __init__(self, allowed, round_digits = None, allow_na = False):

        super().__init__(int, False, allow_na)
        self.allowed = allowed
        self.round_digits = round_digits

class FloatRange(Data):
    """
    Hold characteristics of float data in a range

    PARAMETERS:
    - min_ (int): The minimum value the data can be, inclusive, defaults to None (no minimum)
    - max_ (int): The maximum value the data can be, inclusive, defaults to None (no maximum)
    - round_digits (int/None): The number of digits to round data to before checking (None if don't round)
    """

    def __init__(self, min_ = None, max_ = None, round_digits = None, allow_na = False):

        super().__init__(float, True, allow_na)
        self.min = min_
        self.max = max_
        self.round_digits = round_digits

class FloatList(Data):
    """
    Hold characteristics of float data that can take any value from a list

    PARAMETERS:
    - allowed (list): A list of allowed values data can be
    - round_digits (int/None): The number of digits to round data to before checking (None if don't round)
    """

    def __init__(self, allowed, round_digits = None, allow_na = False):

        super().__init__(float, False, allow_na)
        self.allowed = allowed
        self.round_digits = round_digits

class String(Data):
    """
    Holds characteristics of string data that can take any value from a list

    PARAMETERS:
    - allowed (list): A list of allowed values data can be
    - to_lower (bool): Whether or not to lower the string before checking (will automatically lower allowed values too)
    """

    def __init__(self, allowed, to_lower, allow_na = False):

        super().__init__(str, False, allow_na)
        self.allowed = [item.lower() for item in allowed]
        self.to_lower = to_lower

class Validation:
    """
    Validates inputs or parameters according to their specification
    """

    def __init__(self):
        pass

    def base(self)

    def validate(self, data, spec):

        assert isinstance(spec, Data), "'spec' must be an object descending from the 'Data' class"

    def validate_input(self, prompt, spec):
        """
        Validate inputs (repeatedly ask the user until they abide by the specification)
        """

        acceptable = False
        while not acceptable:
            inp = input(prompt) #may want to change to an integer or whatever so may want to recieve back from function
            acceptable = self.validate(inp, spec)

        return inp