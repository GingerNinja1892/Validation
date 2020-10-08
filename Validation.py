"""
Tools for validating inputs or variables according to specifications detailing what format, datatype, etc. the data must be.

TODO:
- Add common specifications already created
- Change date, time and datetime to use isValid date, time and datetime methods so can call externally
- Change true_false to error if not one of the possibilities
"""

def _round(num, digits):
    """
    Private rounding method which uses the built-in round function but fixes a problem:
    If you call it with the number of digits as 0, it will round to 0 decimal places but leave as a float (so it has a .0 at the end)
    Whereas if you call it without the number of digits, it will round to 0 decimal places but convert to an integer
    But as I dynamically work out digits, I always provide the number of digits even if it is 0 and if it is 0, I want it to be an int
    So I just check this and potentially call it with no arguments accordingly
    """

    return round(num, digits) if digits != 0 else round(num)

class Spec:
    """
    Specifies the format of data in general

    :param type_: The datatype the data must be
    :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
    """

    def __init__(self, type_, extra_values=None):
        """
        Specifies the format of data

        :param type_: The datatype the data must be
        :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
        """

        assert isinstance(type_, type), "param type_ must be a datatype"

        self.type = type_
        self.extra_values = extra_values
        self.msg = "Must be type {}".format(str(type_)[8:-2])
        if extra_values:
            self.msg += " or one of the following: " + ", ".join(["'{}'".format(value) for value in extra_values])

    def __repr__(self):
        return "Spec({})".format(self.msg)

class SpecStr(Spec):
    """
    Specifies the format of a string

    :param allowed_strings: A list of allowed strings. None allows any. Default: None.
    :param allowed_chars: A list of allowed characters. None allows any. Default: None.
    :param to_lower: Whether or not to lower the string before checking. Default: True
    :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
    """

    def __init__(self, allowed_strings=None, allowed_chars=None, to_lower=True, extra_values=None):
        """
        Specifies the format of a string

        :param allowed_strings: A list of allowed strings. None allows any. Default: None.
        :param allowed_chars: A list of allowed characters. None allows any. Default: None.
        :param to_lower: Whether or not to lower the string before checking. Default: True
        :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
        """

        assert isinstance(allowed_strings, list) or allowed_strings is None, "param allowed_strings must be a list or None"
        if allowed_strings is not None:
            assert all([isinstance(item, str) for item in allowed_strings]), "all items in param allowed_strings must be strings"

        assert isinstance(allowed_chars, list) or allowed_chars is None, "param allowed_chars must be a list or None"
        if allowed_chars is not None:
            assert all([isinstance(item, str) and len(item) == 1 for item in allowed_chars]), "all items in param allowed_chars must be strings of length 1"

        super().__init__(str, extra_values)
        self.allowed_strings = [item.lower() for item in allowed_strings] if to_lower and allowed_strings is not None else allowed_strings
        self.allowed_chars = [item.lower() for item in allowed_chars] if to_lower and allowed_chars is not None else allowed_chars
        self.to_lower = to_lower

        if allowed_strings is not None:
            if to_lower:
                self.msg += " and once converted to lower case, must be one of the following: "
            else:
                self.msg += " and must be one of the following: "
            self.msg += ", ".join(["'{}'".format(item) for item in allowed_strings])

        if allowed_chars is not None:
            if to_lower:
                self.msg += " and once converted to lower case, every character must be one of the following: "
            else:
                self.msg += " and every character must be one of the following: "
            self.msg += ", ".join(["'{}'".format(item) for item in allowed_chars])

class SpecNum(Spec):
    """
    Specifies the format of a number

    :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
    :param restrict_to_int: Whether or not to only allow integers. Default: False
    :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
    """

    def __init__(self, round_digits=None, restrict_to_int=False, extra_values=None):
        """
        Specifies the format of a number

        :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
        :param restrict_to_int: Whether or not to only allow integers. Default: False
        :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
        """

        assert round_digits is None or isinstance(round_digits, int), "param round_digits must be an integer or None"

        super().__init__(int if restrict_to_int else float, extra_values)
        self.round_digits = round_digits

        if restrict_to_int:
            self.msg = "Must be an integer"
        else:
            self.msg = "Must be a number"

        if round_digits is not None:
            self.msg = "Once rounded to {} decimal places, m".format(round_digits) + self.msg[1:]

        if extra_values:
            self.msg += " or leave blank"

class SpecNumRange(SpecNum):
    """
    Specifies the format of a number in a range

    :param min_: The minimum valid value. None means there is no minimum. Default: None
    :param max_: The maximum valid value. None means there is no maximum. Default: None
    :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
    :param restrict_to_int: Whether or not to only allow integers. Default: False
    :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
    """

    def __init__(self, min_=None, max_=None, round_digits=None, restrict_to_int=False, extra_values=None):
        """
        Specifies the format of a number in a range

        :param min_: The minimum valid value. None means there is no minimum. Default: None
        :param max_: The maximum valid value. None means there is no maximum. Default: None
        :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
        :param restrict_to_int: Whether or not to only allow integers. Default: False
        :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
        """

        assert isinstance(min_, (int, float)) or min_ is None, "param min_ must be a number or None"
        assert isinstance(max_, (int, float)) or max_ is None, "param max_ must be a number or None"

        super().__init__(round_digits, restrict_to_int, extra_values)
        self.min = min_
        self.max = max_

        if min_ is not None:
            self.msg += ", minimum {}".format(min_)
        if max_ is not None:
            self.msg += ", maximum {}".format(max_)

class SpecNumList(SpecNum):
    """
    Specifies the format of a number from a list of allowed numbers

    :param list_of_allowed: A list of allowed numbers
    :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
    :param restrict_to_int: Whether or not to only allow integers. Default: False
    :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
    """

    def __init__(self, list_of_allowed, round_digits=None, restrict_to_int=False, extra_values=None):
        """
        Specifies the format of a number from a list of allowed numbers

        :param list_of_allowed: A list of allowed numbers
        :param round_digits: The number of digits to round to before checking. None means don't round. Default: None
        :param restrict_to_int: Whether or not to only allow integers. Default: False
        :param extra_values: A list of extra values it can take to always be true, even if not the datatype. Default: None
        """

        assert isinstance(list_of_allowed, (list, tuple)), "param list_of_allowed must be a list or tuple"
        assert all([isinstance(item, int if restrict_to_int else (int, float)) for item in list_of_allowed]), "all items in param list_of_allowed must be numbers"

        super().__init__(round_digits, restrict_to_int, extra_values)
        self.list_of_allowed = list_of_allowed

        self.msg += " that is one of the following: " + ", ".join(["'{}'".format(item) for item in list_of_allowed])

def is_valid(value, spec):
    """
    Return whether or not 'value' is valid according to 'spec' and the validated 'value'

    :param value: The value to validate
    :param spec: A descendant of the 'Spec' class, containing information on how to validate
    :return: Whether or not the value was valid according to the specification
    :return: The value after validation (converted to the right type, lowered if applicable, etc.). This is only valid if the first return value is True.
    """

    assert isinstance(spec, Spec), "param spec must be an object of a 'Spec' class"

    if spec.extra_values and value in spec.extra_values:
        return True, value

    if isinstance(value, str):
        value = value.strip()

    if isinstance(spec, SpecNum):
        # rounds before converting as if it is meant to be an int but it is a float but they have
        # allowed rounding to the nearest whole number, it would error but not when doing this
        try:
            value = float(value)
        except (ValueError, TypeError):
            return False, value
        else:
            if spec.round_digits is not None:
                value = _round(value, spec.round_digits)

    try:
        value = spec.type(value)
    except ValueError:
        return False, value
    else:
        if isinstance(spec, SpecStr) and spec.to_lower:
            value = value.lower()
        if isinstance(spec, SpecNum) and spec.round_digits is not None:
            value = _round(value, spec.round_digits)

        if hasattr(spec, "allowed_strings") and spec.allowed_strings is not None:
            return value in spec.allowed_strings, value

        if hasattr(spec, "list_of_allowed") and spec.list_of_allowed is not None:
            return value in spec.list_of_allowed, value

        if hasattr(spec, "allowed_chars") and spec.allowed_chars is not None:
            return all([char in spec.allowed_chars for char in value]), value

        if isinstance(spec, SpecNumRange):
            if spec.min is not None and spec.max is not None:
                return spec.min <= value <= spec.max, value
            if spec.min is not None:
                return spec.min <= value, value
            if spec.max is not None:
                return value <= spec.max, value

    return True, value

def validate_input(spec, prompt=None):
    """
    Repeatedly ask the user for input until their input is valid according to 'spec' and return their validated input

    :param spec: A descendant of the 'Spec' class, containing information on how to validate
    :param prompt: The prompt to display to the user before asking them to input. None displays nothing. Default: None
    :return: The valid value the user input
    """

    acceptable = False
    while not acceptable:
        acceptable, value = is_valid(input(prompt) if prompt is not None else input(), spec)
        if not acceptable:
            print(spec.msg)

    return value

def assert_valid(value, spec, name=None):
    """
    Throw an assertion error if 'value' is invalid according to 'spec', otherwise return it

    :param value: The value to validate
    :param spec: A descendant of the 'Spec' class, containing information on how to validate
    :param name: The name to reference the value so it is clear what is invalid in error messages. None just displays the error message. Default: None
    :return value: If it hasn't thrown an assertion error, returns the valid value after normalisation
    """

    valid, value = is_valid(value, spec)

    assert valid, spec.msg if name is None else str(name).strip().lower() + ": " + spec.msg

    return value

def true_false(prompt=None, extra_values=None):
    """
    Repeatedly ask the user for an input until they input a boolean-like value and return the boolean version

    :param prompt: The prompt to display to the user before asking them to input. None will not display anything. Default: None
    :param extra_values: A list of extra values it can take to be None. Default: None
    :return: True or False depending on the user's input or None if extra_values and they input one of these
    """

    value = validate_input(specTrueFalse, prompt)

    if extra_values is not None and value in extra_values:
        return None

    if value in ["f", "false", "n", "no", "0", "off", "disabled", "disable"]:
        return False

    return True

def date(prompt=None, enforce=True, form="exact", fill_0s=True):
    """
    Repeatedly ask the user for a year, month and day until they input valid values and return this in a defined format

    :param prompt: Message to display to the user before asking them for inputs. Default: None
    :param enforce: Whether or not to enforce valid dates. If False, will allow empty inputs. Default: True
    :param form: The form to output the date in. Default: 'exact'. Must be one of the following:
        - 'exact': year-month-day
        - 'uk': day/month/year
        - 'us': month/day/year
        - 'long': day_with_suffix month_as_word, year
    :param fill_0s: Whether or not to fill numerical dates with leading 0s. Doesn't apply to 'long' form
    """

    extras = None if enforce else [""]

    form = assert_valid(form, SpecStr(["exact", "uk", "us", "long"]), "param form")

    if prompt is not None:
        print(prompt, "\n")

    year = validate_input(SpecNumRange(restrict_to_int=True, extra_values=extras), "Year: " if enforce else "Year (can leave blank): ")

    if enforce:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            leap_year = True
        else:
            leap_year = False

    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    allowed = months.copy()
    allowed.extend(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])

    month = validate_input(SpecStr(allowed, extra_values=extras), "Month: " if enforce else "Month (can leave blank): ")
    if month in months:
        month = months.index(month) + 1
    elif month in allowed:
        month = int(month)

    days = 28 if month == 2 and (not enforce or not leap_year) else \
        29 if month == 2 and (not enforce or leap_year) else \
        30 if month == 4 or month == 6 or month == 9 or month == 11 else \
        31

    day = validate_input(SpecNumRange(1, days, None, True, extras), "Date/day: " if enforce else "Date/day (can leave blank): ")

    if year is None:
        year = "?"

    if month is None:
        month = "?"

    if day is None:
        day = "?"

    if form == "long":

        suffix = "st" if day % 10 == 1 else "nd" if day % 10 == 2 else "rd" if day % 10 == 3 else "th"
        month = months[month - 1]
        month = "".join([month[i].upper() if i == 0 else month[i] for i in range(len(month))])

        return "{}{} {}, {}".format(day, suffix, month, year)

    if fill_0s and month != "?" and day != "?":
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
    Repeatedly ask the user to input hours, minutes and seconds until they input valid values and return this in a defined format

    :param prompt: Message to display to the user before asking them for inputs. Default: None
    :param output_hour_clock: Whether to output in 24 hour clock or in 12 hour clock with AM/PM. Default: 24
    :param milli_seconds: Whether or not to allow more accuracy in seconds. Default: False
    :param fill_0s: Whether or not to fill numerical times with leading 0s. Default: False
    :param allow_na: Whether or not to allow empty inputs too. Default: False
    """

    extras = None if allow_na else [""]

    output_hour_clock = assert_valid(output_hour_clock, SpecNumList([12, 24], None, True), "param output_hour_clock")

    if prompt is not None:
        print(prompt, "\n")

    input_hour_clock = validate_input(SpecNumList([12, 24], None, True), "Input hour clock (12/24): ")

    if input_hour_clock == 12:
        hours = validate_input(SpecNumRange(1, 12, None, True, extras), "Hours (12 hour clock): ")
        period = validate_input(SpecStr(["am", "pm"], extra_values=extras), "AM or PM? ")
        if hours == 12:
            hours = 0
        if period == "pm":
            hours += 12
    else:
        hours = validate_input(SpecNumRange(0, 23, None, True, extras), "Hours (24 hour clock): ")

    minutes = validate_input(SpecNumRange(0, 59, None, True, extras), "Minutes: ")

    if milli_seconds:
        seconds = validate_input(SpecNumRange(0, 59.999999, 6, False, extras), "Seconds including decimal: ")
    else:
        seconds = validate_input(SpecNumRange(0, 59, 0, True, extras), "Seconds: ")

    if hours is not None and output_hour_clock == 12:
        if hours < 12:
            period = "AM"
        else:
            period = "PM"

        hours %= 12
        if hours == 0:
            hours = 12

    if fill_0s:
        if hours is not None and hours < 10:
            hours = "0" + str(hours)
        if minutes is not None and minutes < 10:
            minutes = "0" + str(minutes)
        if seconds is not None and seconds < 10:
            seconds = "0" + str(seconds)

    to_return = "{}:{}:{}".format(hours, minutes, seconds)

    if output_hour_clock == 12:
        to_return += " {}".format(period)

    return to_return

def datetime(prompt=None, enforce=True, form="exact", milli_seconds=False, fill_0s=True):
    """
    Repeatedly ask the user to input a year, month, day, hours, minutes and seconds until they input valid values and return this in a defined format

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

specTrueFalse = SpecStr(["t", "true", "f", "false", "y", "yes", "n", "no", "0", "1", "on", "off", "enabled", "enable", "disabled", "disable"])
specDay = SpecNumRange(1, 31, restrict_to_int=True)
specMonth = SpecNumRange(1, 12, restrict_to_int=True)
specYear = SpecNumRange(1, restrict_to_int=True)
specHour = SpecNumRange(0, 23, restrict_to_int=True)
specMinuteSecond = SpecNumRange(0, 59, restrict_to_int=True)
