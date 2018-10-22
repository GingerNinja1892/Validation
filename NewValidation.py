"""
TODO:
Add error messages
Add date functions from 'Validation'
Add old functions for backwards compatability
"""

def _my_round(num, digits):
    return round(num, digits) if digits != 0 else round(num)

class NA:
    """
    Represents the absence of a value - not applicable - N/A
    """
    def __init__(self):
        pass
    def __repr__(self):
        return "N/A"

class Spec:
    """
    Specifies the format of data
    :param type_: The datatype the data must be
    :param allow_na: Whether or not to allow the absence of data
    """

    def __init__(self, type_, allow_na=False):
        self.type = type_
        self.allow_na = allow_na

class StrSpec(Spec):
    """
    Specifies the format of a string
    :param list_of_allowed: A list of allowed strings
    :param to_lower: Whether or not to lower the string before checking
    :param allow_na: Whether or not to allow the absence of data
    """

    def __init__(self, list_of_allowed, to_lower, allow_na=False):
        super().__init__(str, allow_na)
        self.list_of_allowed = list_of_allowed
        self.to_lower = to_lower

class NumberSpec(Spec):
    """
    Specifies the format of a number
    :param type_: The type the data must be. Float allows any number. Default: float
    :param round_digits: The number of digits to round to before checking. None means don't
    round. Default: None
    :param allow_na: Whether or not to allow the absence of data
    """

    def __init__(self, type_=float, round_digits=None, allow_na=False):
        super().__init__(self, type_, allow_na)
        self.round_digits = round_digits

class IntRange(NumberSpec):
    """
    Specifies the format of an integer in a range
    :param min_: The minimum valid value
    :param max_: The maximum valid value
    :param round_digits: The number of digits to round to before checking. None means don't
    round. Default: None
    :param allow_na: Whether or not to allow the absence of data
    """

    def __init__(self, min_=None, max_=None, round_digits=None, allow_na=False):
        super().__init__(int, round_digits, allow_na)
        self.min = min_
        self.max = max_

class IntList(NumberSpec):
    """
    Specifies the format of an integer from a list of allowed integers
    :param list_of_allowed: A list of allowed integers
    :param round_digits: The number of digits to round to before checking. None means don't
    round. Default: None
    :param allow_na: Whether or not to allow the absence of data
    """

    def __init__(self, list_of_allowed, round_digits=None, allow_na=False):
        super().__init__(int, round_digits, allow_na)
        self.list_of_allowed = list_of_allowed

class FloatRange(NumberSpec):
    """
    Specifies the format of a float in a range
    :param min_: The minimum valid value
    :param max_: The maximum valid value
    :param round_digits: The number of digits to round to before checking. None means don't
    round. Default: None
    :param allow_na: Whether or not to allow the absence of data
    """

    def __init__(self, min_=None, max_=None, round_digits=None, allow_na=False):
        super().__init__(float, round_digits, allow_na)
        self.min = min_
        self.max = max_

class FloatList(NumberSpec):
    """
    Specifies the format of a float from a list of allowed floats
    :param list_of_allowed: A list of allowed floats
    :param round_digits: The number of digits to round to before checking. None means don't
    round. Default: None
    :param allow_na: Whether or not to allow the absence of data
    """

    def __init__(self, list_of_allowed, round_digits=None, allow_na=False):
        super().__init__(float, round_digits, allow_na)
        self.list_of_allowed = list_of_allowed

def is_valid(value, spec):
    """
    Validate a parameter ('value') according to a specification ('spec') made from one of the
    above classes
    :param value: The value to validate
    :param spec: A descendant of the 'Spec' class, containing information on how to validate
    :return: Whether or not the value was valid according to the specification
    :return: The value after validation (converted to the right type, lowered if applicable,
    etc.). This is only valid if the first return value is True.
    """

    assert isinstance(spec, Spec), "param spec must be an object descending from class Spec"

    if isinstance(value, str):
        value = value.strip()

        if spec.allow_na and value == "":
            return True, NA()

    try:
        value = spec.type(value)
    except ValueError:
        return False, value
    else:
        if isinstance(spec, StrSpec) and spec.to_lower:
            value = value.lower()
        if isinstance(spec, NumberSpec) and spec.round_digits is not None:
            value = _my_round(value, spec.round_digits)

        if hasattr(spec, "list_of_allowed") and spec.list_of_allowed:
            return value in spec.list_of_allowed, value

        if isinstance(spec, (IntRange, FloatRange)):
            if spec.min is not None and spec.max is not None:
                return spec.min <= value <= spec.max, value
            if spec.min is not None:
                return spec.min <= value, value
            if spec.max is not None:
                return value <= spec.max, value

    return True, value

def validate_input(prompt, spec):
    """
    Validate inputs from the user according to a specification - repeadly ask the user until they
    provide a valid response
    :param prompt: The prompt to display to the user before asking them to input
    :param spec: A descendant of the 'Spec' class, containing information on how to validate
    :return: The valid value the user input
    """

    acceptable = False
    while not acceptable:
        acceptable, value = is_valid(input(prompt), spec)
        if not acceptable:
            print(spec.error)

    return value

def true_false(prompt, allow_na=False):
    """
    Repeatedly asks the user for an input until they input a boolean-like value and converts
    this into a boolean
    """

    value = validate_input(prompt, StrSpec(["t", "true", "f", "false", "y", "yes", "n", "no", "0", "1"], True, allow_na))

    if isinstance(value, NA):
        return None

    if value == "f" or value == "false" or value == "n" or value == "no" or value == "0":
        return False

    return True