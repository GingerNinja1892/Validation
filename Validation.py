"""
Validate inputs or parameters according to a specification containing the format required

Standard use:
Create a specification using the class 'Spec' or a descendant of it (all start with 'Spec') and pass this to either 'is_valid' to validate a parameter or 'validate_input' to validate an input or 'assert_valid' to throw an assertion error if invalid

TODO:
Test
Write better documentation including docstrings
Write README
Add licence, etc.
Publish on PIP
"""


def _my_round(num, digits):
    return round(num, digits) if digits != 0 else round(num)


class NA:
    """
    The absence of a value usually created when an empty string is input which could represent not applicable
    """

    def __init__(self):
        pass

    def __repr__(self):
        return "N/A"


class Spec:
    """
    Specifies the format of data

    :param type_: The datatype the data must be
    :param allow_na: Whether or not to allow the absence of data. Default: False
    """

    def __init__(self, type_, allow_na=False):

        assert isinstance(type_, type), "param type_ must be a datatype"

        self.type = type_
        self.allow_na = allow_na
        self.spec = "Must be type {}".format(str(type_)[8:-2])
        if allow_na:
            self.spec += " or leave blank"

    def __repr__(self):
        return "Spec({})".format(self.spec)


class SpecStr(Spec):
    """
    Specifies the format of a string

    :param list_of_allowed: A list of allowed strings
    :param to_lower: Whether or not to lower the string before checking. Default: True
    :param allow_na: Whether or not to allow the absence of data. Default: False
    """

    def __init__(self, list_of_allowed, to_lower=True, allow_na=False):

        assert isinstance(
            list_of_allowed, list), "param list_of_allowed must be a list"
        assert all([isinstance(item, str) for item in list_of_allowed]
                   ), "all items in param list_of_allowed must be strings"

        super().__init__(str, allow_na)
        self.list_of_allowed = [
            item.lower() for item in list_of_allowed] if to_lower else list_of_allowed
        self.to_lower = to_lower

        if to_lower:
            self.spec += " and once converted to lower case, must be one of the following: "
        else:
            self.spec += " and must be one of the following: "

        self.spec += ", ".join(["'{}'".format(item)
                                for item in list_of_allowed])


class SpecNum(Spec):
    """
    Specifies the format of a number

    :param type_: The type the data must be. Float allows any number. Default: float
    :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
    :param allow_na: Whether or not to allow the absence of data. Default: False
    """

    def __init__(self, type_=float, round_digits=None, allow_na=False):

        assert round_digits is None or isinstance(
            round_digits, int), "param round_digits must be an integer or None"

        super().__init__(type_, allow_na)
        self.round_digits = round_digits

        if type_ == int:
            self.spec = "Must be an integer"
        else:
            self.spec = "Must be a number"

        if round_digits is not None:
            self.spec = "Once rounded to {} decimal places, m".format(
                round_digits) + self.spec[1:]

        if allow_na:
            self.spec += " or leave blank"


class SpecIntRange(SpecNum):
    """
    Specifies the format of an integer in a range

    :param min_: The minimum valid value
    :param max_: The maximum valid value
    :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
    :param allow_na: Whether or not to allow the absence of data. Default: False
    """

    def __init__(self, min_=None, max_=None, round_digits=None, allow_na=False):

        assert isinstance(min_, int) or min_ is None, "param min_ must be an integer or None"
        assert isinstance(max_, int) or max_ is None, "param max_ must be an integer or None"

        super().__init__(int, round_digits, allow_na)
        self.min = min_
        self.max = max_

        if min_ is not None:
            self.spec += ", minimum {}".format(min_)
        if max_ is not None:
            self.spec += ", maximum {}".format(max_)


class SpecIntList(SpecNum):
    """
    Specifies the format of an integer from a list of allowed integers

    :param list_of_allowed: A list of allowed integers
    :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
    :param allow_na: Whether or not to allow the absence of data. Default: False
    """

    def __init__(self, list_of_allowed, round_digits=None, allow_na=False):

        assert isinstance(
            list_of_allowed, list), "param list_of_allowed must be a list"
        assert all([isinstance(item, int) for item in list_of_allowed]
                   ), "all items in param list_of_allowed must be integers"

        super().__init__(int, round_digits, allow_na)
        self.list_of_allowed = list_of_allowed

        self.spec += " that is one of the following: " + \
            ", ".join(["'{}'".format(item) for item in list_of_allowed])


class SpecFloatRange(SpecNum):
    """
    Specifies the format of a float in a range

    :param min_: The minimum valid value
    :param max_: The maximum valid value
    :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
    :param allow_na: Whether or not to allow the absence of data. Default: False
    """

    def __init__(self, min_=None, max_=None, round_digits=None, allow_na=False):

        assert isinstance(min_, (float, int)) or min_ is None, "param min_ must be a number or None"
        assert isinstance(max_, (float, int)) or max_ is None, "param max_ must be a number or None"

        super().__init__(float, round_digits, allow_na)
        self.min = min_
        self.max = max_

        if min_ is not None:
            self.spec += ", minimum {}".format(min_)
        if max_ is not None:
            self.spec += ", maximum {}".format(max_)


class SpecFloatList(SpecNum):
    """
    Specifies the format of a float from a list of allowed floats

    :param list_of_allowed: A list of allowed floats
    :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
    :param allow_na: Whether or not to allow the absence of data. Default: False
    """

    def __init__(self, list_of_allowed, round_digits=None, allow_na=False):

        assert isinstance(
            list_of_allowed, list), "param list_of_allowed must be a list"
        assert all([isinstance(item, float) for item in list_of_allowed]
                   ), "all items in param list_of_allowed must be floats"

        super().__init__(float, round_digits, allow_na)
        self.list_of_allowed = list_of_allowed

        self.spec += " that is one of the following: " + \
            ", ".join(["'{}'".format(item) for item in list_of_allowed])


def is_valid(value, spec):
    """
    Validate a parameter ('value') according to a specification ('spec') made from one of the above classes

    :param value: The value to validate
    :param spec: A descendant of the 'Spec' class, containing information on how to validate
    :return: Whether or not the value was valid according to the specification
    :return: The value after validation (converted to the right type, lowered if applicable, etc.). This is only valid if the first return value is True.
    """

    assert isinstance(
        spec, Spec), "param spec must be an object of a 'Spec' class"

    if value is None and spec.allow_na:
        return True, None

    if isinstance(value, str):
        value = value.strip()

        if spec.allow_na and value == "":
            return True, NA()

    if isinstance(spec, SpecNum):
        # rounds before converting as if it is meant to be an int but it is a float but they have
        # allowed rounding to the nearest whole number, it would error but not when doing this
        try:
            value = float(value)
        except ValueError:
            return False, value
        else:
            if spec.round_digits is not None:
                value = _my_round(value, spec.round_digits)

    try:
        value = spec.type(value)
    except ValueError:
        return False, value
    else:
        if isinstance(spec, SpecStr) and spec.to_lower:
            value = value.lower()
        if isinstance(spec, SpecNum) and spec.round_digits is not None:
            value = _my_round(value, spec.round_digits)

        if hasattr(spec, "list_of_allowed") and spec.list_of_allowed:
            return value in spec.list_of_allowed, value

        if isinstance(spec, (SpecIntRange, SpecFloatRange)):
            if spec.min is not None and spec.max is not None:
                return spec.min <= value <= spec.max, value
            if spec.min is not None:
                return spec.min <= value, value
            if spec.max is not None:
                return value <= spec.max, value

    return True, value


def assert_valid(value, spec, name=None):
    """
    Assert that a paramater ('value') is valid according to a specification ('spec') made from one of the above classes
    If the message is invalid, throws an assertion error with message. If valid, returns the normalized value

    :param value: The value to validate
    :param spec: A descendant of the 'Spec' class, containing information on how to validate
    :param name: The name to reference the value so it is clear what is invalid. Default: None
    :return value: If it hasn't thrown an assertion error, returns the valid value after normalisation
    """

    valid, value = is_valid(value, spec)

    assert valid, spec.spec if name is None else str(
        name).strip().lower() + ": " + spec.spec

    return value


def validate_input(prompt, spec):
    """
    Validate inputs from the user according to a specification - repeadly ask the user until they provide a valid response

    :param prompt: The prompt to display to the user before asking them to input
    :param spec: A descendant of the 'Spec' class, containing information on how to validate
    :return: The valid value the user input
    """

    acceptable = False
    while not acceptable:
        acceptable, value = is_valid(input(prompt), spec)
        if not acceptable:
            print(spec.spec)

    return value


def true_false(prompt, allow_na=False):
    """
    Repeatedly asks the user for an input until they input a boolean-like value and converts this into a boolean

    :param prompt: The prompt to display to the user before asking them to input
    :param allow_na: Whether or not to allow the absence of a value. Default: False
    :return: True or False depending on the user's input or None if allow_na and they input nothing
    """

    value = validate_input(prompt, SpecStr(
        ["t", "true", "f", "false", "y", "yes", "n", "no", "0", "1"], True, allow_na))

    if isinstance(value, NA):
        return None

    if value == "f" or value == "false" or value == "n" or value == "no" or value == "0":
        return False

    return True


def date(prompt=None, enforce=True, form="exact", fill_0s=True):
    """
    Get input from the user for a year, month and day

    :param prompt: Message to display to the user before asking them for inputs. Default: None
    :param enforce: Whether or not to enforce valid dates. If False, will allow empty inputs. Default: True
    :param form: The form to output the date in. If 'enforce' is 'False', it is always 'exact'. Default: 'exact'. Must be one of the following:
        - 'exact': year-month-day
        - 'uk': day/month/year
        - 'us': month/day/year
        - 'long': day_with_suffix month_as_word, year
    :param fill_0s: Whether or not to fill numerical dates with leading 0s. Doesn't apply to 'long' form
    """

    form = assert_valid(form, SpecStr(
        ["exact", "uk", "us", "long"], True), "param form")

    if prompt is not None:
        print(prompt, "\n")

    year = validate_input("Year: ", SpecIntRange(
        None, None, None, not enforce))

    if enforce:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            leap_year = True
        else:
            leap_year = False

    months = ["jan", "feb", "mar", "apr", "may", "jun",
              "jul", "aug", "sep", "oct", "nov", "dec"]
    allowed = months.copy()
    allowed.extend(["1", "2", "3", "4", "5", "6",
                    "7", "8", "9", "10", "11", "12"])

    month = validate_input("Month: ", SpecStr(allowed, True, not enforce))
    if month in months:
        month = months.index(month) + 1
    elif month in allowed:
        month = int(month)

    days = 28 if month == 2 and not leap_year else \
        29 if month == 2 and leap_year else \
        30 if month == 4 or month == 6 or month == 9 or month == 11 else \
        31

    day = validate_input("Date (day): ", SpecIntRange(
        1, days, None, not enforce))

    if enforce:
        form = "exact"

    if form == "long":

        suffix = "st" if day % 10 == 1 else "nd" if day % 10 == 2 else "rd" if day % 10 == 3 else "th"
        month = months[month - 1]
        month = "".join([month[i].upper() if i == 0 else month[i]
                         for i in range(len(month))])

        return "{}{} {}, {}".format(day, suffix, month, year)

    if fill_0s and not isinstance(month, NA) and not isinstance(day, NA):
        if month < 10:
            month = "0" + str(month)
        if day < 10:
            day = "0" + str(day)

    if form == "exact":
        return "{}-{}-{}".format(year, month, day)

    if form == "us":
        return "{}/{}/{}".format(month, day, year)

    return "{}/{}/{}".format(day, month, year)


def time(prompt=None, output_hour_clock=24, milli_seconds=False, fill_0s=True, allow_na=False):
    """
    Get input from the user for an hour, minute, second and optionally milli seconds

    :param prompt: Message to display to the user before asking them for inputs. Default: None
    :param output_hour_clock: Whether to output in 24 hour clock or in 12 hour clock with AM/PM. Default: 24
    :param milli_seconds: Whether or not to allow more accuracy in seconds. Default: False
    :param fill_0s: Whether or not to fill numerical times with leading 0s. Default: False
    """

    output_hour_clock = assert_valid(output_hour_clock, SpecIntList([12, 24]), "param output_hour_clock")

    if prompt is not None:
        print(prompt, "\n")

    input_hour_clock = validate_input("Input hour clock (12/24): ", SpecIntList([12, 24]))

    if input_hour_clock == 12:
        hours = validate_input("Hours (12 hour clock): ", SpecIntRange(1, 12, None, allow_na))
        period = validate_input("AM or PM? ", SpecStr(["am", "pm"], True, allow_na))
        if hours == 12:
            hours = 0
        if period == "pm":
            hours += 12
    else:
        hours = validate_input("Hours (24 hour clock): ", SpecIntRange(0, 23, None, allow_na))

    minutes = validate_input("Minutes: ", SpecIntRange(0, 59, None, allow_na))

    if milli_seconds:
        seconds = validate_input("Seconds including decimal: ", SpecFloatRange(0, 59.999999, 6, allow_na))
    else:
        seconds = validate_input("Seconds: ", SpecIntRange(0, 59, 0, allow_na))

    if not isinstance(hours, NA) and output_hour_clock == 12:
        if hours < 12:
            period = "AM"
        else:
            period = "PM"

        hours %= 12
        if hours == 0:
            hours = 12

    if fill_0s:
        if not isinstance(hours, NA) and hours < 10:
            hours = "0" + str(hours)
        if not isinstance(minutes, NA) and minutes < 10:
            minutes = "0" + str(minutes)
        if not isinstance(seconds, NA) and seconds < 10:
            seconds = "0" + str(seconds)

    to_return = "{}:{}:{}".format(hours, minutes, seconds)

    if output_hour_clock == 12:
        to_return += " {}".format(period)

    return to_return

def datetime(prompt=None, enforce=True, form="exact", milli_seconds=False, fill_0s=True):
    """
    Get input from the user for a year, month, day, hours, minutes and seconds

    :param prompt: Message to display to the user before asking them for inputs. Default: None
    :param enforce: Whether or not to enforce valid dates. If False, will allow empty inputs. Default: True
    :param form: The form to output the datetime in. Default: exact
        - 'exact': year-month-day hour_in_24_hour_clock:minute:second
        - 'long': day_with_suffix month_as_word, year hour_in_12_hour_clock:minute:second AM_or_PM
    :param milli_seconds: Whether or not to allow more accuracy when inputting seconds. Default: False
    :param fill_0s: Whether or not to fill numerical datetimes with leading 0s. Default: True
    """

    form = assert_valid(form, SpecStr(["exact", "long"]), "param form")

    if prompt is not None:
        print(prompt, "\n")

    date_ = date(None, enforce, form, fill_0s)
    time_ = time(None, 24 if form == "exact" else 12, milli_seconds, fill_0s, not enforce)

    return "{} {}".format(date_, time_)
