"""
TODO:
Add error messages
Add date functions from 'Validation'
"""

def my_round(num, digits):
    return round(num, digits) if digits != 0 else round(num)

class NA:
    def __init__(self):
        pass
    def __repr__(self):
        return "N/A"

class Spec:
    """
    Specifies the format of data
    """

    def __init__(self, type_, allow_na=False):

        self.type = type_
        self.allow_na = allow_na

class StrSpec(Spec):
    """
    Specifies the format of a string
    """

    def __init__(self, list_of_allowed, to_lower, allow_na=False):

        super().__init__(str, allow_na)
        self.list_of_allowed = list_of_allowed
        self.to_lower = to_lower

class NumberSpec(Spec):
    """
    Specifies the format of a number
    """

    def __init__(self, type_override=float, round_digits=None, allow_na=False):

        super().__init__(self, type_override, allow_na)
        self.round_digits = round_digits

class IntRange(NumberSpec):
    """
    Specifies the format of an integer in a range
    """

    def __init__(self, min_=None, max_=None, round_digits=None, allow_na=False):

        super().__init__(int, round_digits, allow_na)
        self.min = min_
        self.max = max_

class IntList(NumberSpec):
    """
    Specifies the format of an integer from a list of allowed integers
    """

    def __init__(self, list_of_allowed, round_digits=None, allow_na=False):

        super().__init__(int, round_digits, allow_na)
        self.list_of_allowed = list_of_allowed

class FloatRange(NumberSpec):
    """
    Specifies the format of a float in a range
    """

    def __init__(self, min_=None, max_=None, round_digits=None, allow_na=False):

        super().__init__(float, round_digits, allow_na)
        self.min = min_
        self.max = max_

class FloatList(NumberSpec):
    """
    Specifies the format of a float from a list of allowed floats
    """

    def __init__(self, list_of_allowed, round_digits=None, allow_na=False):

        super().__init__(float, round_digits, allow_na)
        self.list_of_allowed = list_of_allowed

def is_valid(value, spec):
    """
    Validates a parameter according to a specification
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
            value = my_round(value, spec.round_digits)

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
    Validates inputs according to a specification
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