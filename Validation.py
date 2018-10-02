#TODO: Test

class Validation:
    """
    Validation class to create validation functions with lots of functionality
    """

    def __init__(self):

        self.methods = {
            "int range": self.__int_range,
            "int list": self.__int_list,
            "float range": self.__float_range,
            "float list": self.__float_list,
            "str list": self.__str_list
        }

    def base(self, key, prompt, error, unknown, na, *args):
        """
        Only entry point. For creating custom validation functions
        """

        if unknown:
            error += " or 'unknown'"
        if na:
            error += " or 'n/a'"

        acceptable = False
        while not acceptable:

            var = input(prompt).strip()

            if var == "":
                var = "n/a"

            if (unknown and var.lower() == "unknown") or (na and var.lower() == "n/a"):
                acceptable = True
            else:
                if key in self.methods:
                    acceptable, var = self.methods[key](var, *args)
                else:
                    key(var, *args)
            
            if not acceptable:
                print(error)
        
        return var
    
    def __within_bounds(self, var, *limits):
        """
        Helper function for checking whether 'var' is within 'limits' where 'limits' is a tuple of a minimum and maximum where either can be 'None'
        """

        minimum, maximum = limits

        if (minimum is not None and maximum is not None and minimum <= var <= maximum) or (minimum is not None and maximum is None and not var < minimum) or (maximum is not None and minimum is None and not var > maximum) or (maximum is None and minimum is None):
            return True
        else:
            return False
    
    def __int_range(self, var, *limits):

        try:
            var = int(var)
        except ValueError:
            return False, var
        else:
            return self.__within_bounds(var, *limits), var
    
    def __int_list(self, var, *_list):

        try:
            var = int(var)
        except ValueError:
            return False, var
        else:
            if var in _list:
                return True, var
            else:
                return False, var
    
    def __float_range(self, var, *limits):

        try:
            var = float(var)
        except ValueError:
            return False, var
        else:
            return self.__within_bounds(var, *limits), var
    
    def __float_list(self, var, *args):

        try:
            var = float(var)
        except ValueError:
            return False, var
        else:
            if args[1]:
                var = round(var, args[1])
            elif args[1] == 0:
                var = round(var)

            if var in args[0]:
                return True, var
            else:
                return False, var
    
    def __str_list(self, var, *args):

        if args[1]:
            var = var.lower()
        
        if var in args[0]:
            return True, var
        else:
            return False, var

base = Validation().base

def int_range(prompt, minimum = None, maximum = None, unknown = False, na = False):
    """
    Repeatedly asks the user for an input until they input a whole number within the minimum and maximum provided (inclusive)

    PARAMETERS:
    - prompt (str): The message to display when asking for the input
    - minimum (int/'None'): The minimum value to accept. DEFAULT: None
    - maximum (int/'None'): The maximum value to accept. DEFAULT: None
    - unknown (bool): Whether or not to allow 'unknown' as an input
    - na (bool): Whether or not to allow 'n/a' as an input

    RETURNS:
    - input (int/['unknown']/['n/a']): What the user entered
    """

    error = "Must be a whole number"
    if minimum is not None:
        error += ", minimum: " + str(minimum)
    if maximum is not None:
        error += ", maximum: " + str(maximum)

    return base("int range", prompt, error, unknown, na, minimum, maximum)

def int_list(prompt, _list, unknown = False, na = False):
    """
    Repeatedly asks the user for an input until they input a whole number contained in the list provided

    PARAMETERS:
    - prompt (str): The message to display when asking for the input
    - _list (list): The list of allowed integers of int type
    - unknown (bool): Whether or not to allow 'unknown' as an input
    - na (bool): Whether or not to allow 'n/a' as an input

    RETURNS:
    - input (int/['unknown']/['n/a']): What the user entered
    """

    return base("int list", prompt, "Must be a whole number and one of the following: " + str(_list).replace("[","").replace("]",""), unknown, na, _list)

def float_range(prompt, minimum = None, maximum = None, unknown = False, na = False):
    """
    Repeatedly asks the user for an input until they input a number within the minimum and maximum provided (inclusive)

    PARAMETERS:
    - prompt (str): The message to display when asking for the input
    - minimum (float/'None'): The minimum value to accept. DEFAULT: None
    - maximum (float/'None'): The maximum value to accept. DEFAULT: None
    - unknown (bool): Whether or not to allow 'unknown' as an input
    - na (bool): Whether or not to allow 'n/a' as an input

    RETURNS:
    - input (float/['unknown']/['n/a']): What the user entered
    """

    error = "Must be a number"
    if minimum is not None:
        error += ", minimum: " + str(minimum)
    if maximum is not None:
        error += ", maximum: " + str(maximum)
    
    return base("float range", prompt, error, unknown, na, minimum, maximum)

def float_list(prompt, _list, num_digits = None, unknown = False, na = False):
    """
    Repeatedly asks the user for an input until they input a number contained in the list provided

    PARAMETERS:
    - prompt (str): The message to display when asking for the input
    - _list (list): The list of allowed numbers of float type
    - unknown (bool): Whether or not to allow 'unknown' as an input
    - na (bool): Whether or not to allow 'n/a' as an input

    RETURNS:
    - input (float/['unknown']/['n/a']): What the user entered
    """

    return base("float list", prompt, "Must be a number and one of the following: " + str(_list).replace("[","").replace("]",""), unknown, na, _list, num_digits)

def str_list(prompt, _list, _lower = True, unknown = False, na = False):
    """
    Repeatedly asks the user for an input until they input a value contained in the list provided

    PARAMETERS:
    - prompt (str): The message to display when asking for the input
    - _list (list): The list of allowed values of str type
    - unknown (bool): Whether or not to allow 'unknown' as an input
    - na (bool): Whether or not to allow 'n/a' as an input

    RETURNS:
    - input (str/['unknown']/['n/a']): What the user entered
    """

    return base("str list", prompt, "Must be one of the following: " + str(_list).replace("[","").replace("]","").replace("'",""), unknown, na, _list, _lower)

def true_false(prompt, unknown = False, na = False):
    """
    Repeatedly asks the user for an input until they input a boolean-like value, then outputs their answer as a bool. If 'unknown' or 'n/a' allowed and the user enters them, will output 'None'

    PARAMETERS:
    - prompt (str): The message to display when asking for the input
    - unknown (bool): Whether or not to allow 'unknown' as an input
    - na (bool): Whether or not to allow 'n/a' as an input

    RETURNS:
    - input (bool/'None'): Either 'True', 'False', or 'None'
    """

    ans = str_list(prompt, ["y", "yes", "t", "true", "f", "false", "n", "no"], True, unknown, na)
    if ans == "y" or ans == "yes" or ans == "t" or ans == "true":
        return True
    elif ans == "n" or ans == "no" or ans == "f" or ans == "false":
        return False
    else:
        return None

def files(name):
    """
    Returns whether or not a file exists in the current path.

    PARAMETERS:
    - name (str): The name of the file including extension

    RETURNS:
    - exists (bool): Whether or not the file exists
    """

    try:
        f = open(name)
    except FileNotFoundError:
        return False
    else:
        f.close()
        return True

def date(prompt, form = "UK", fill_0s = False):
    """
    Gets input from the user for a year, month and day. The days allowed are restricted depending on the month and year, e.g.: Feb 29th cannot be entered unless a leap year. All fields must be filled in - none can be 'unknown' or 'n/a'.

    PARAMETERS:
    - prompt (str): What to display before asking the user for input
    - form (str): The form of output, one of the following:
        - 'exact': year-month-day
        - 'uk': day/month/year
        - 'us': month/day/year
        - 'long': <day with suffix> <month as text>, <year>
    - fill_0s (bool): Whether or not to add leading 0s to days and months. Doesn't apply in 'long' form

    RETURNS:
    - date (str): The date entered in the form specified
    """

    form = form.lower()

    print(prompt+"\n")

    year = int_range("Year: ")

    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        leap_year = True
    else:
        leap_year = False
    
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    allowed = months
    allowed.extend(["1","2","3","4","5","6","7","8","9","10","11","12"])
    month = str_list("Month: ", allowed)
    if month in months:
        month = months.index(month) + 1
    else:
        month = int(month)

    days = 28 if month == 2 and not leap_year else \
           29 if month == 2 and leap_year else \
           30 if month == 4 or month == 6 or month == 9 or month == 11 else \
           31
    
    day = int_range("Date (day): ", 1, days)

    if form == "long":

        suffix = "st" if day % 10 == 1 else "nd" if day % 10 == 2 else "rd" if day % 10 == 3 else "th"
        month = months[month - 1]
        month = "".join([month[i].upper() if i == 0 else month[i] for i in range(len(month))])

        return "{}{} {}, {}".format(day, suffix, month, year)
    
    else:
        if fill_0s:
            if month < 10:
                month = "0" + str(month)
            if day < 10:
                day = "0" + str(day)

        if form == "exact":
            return "{}-{}-{}".format(year, month, day)

        elif form == "uk":
            return "{}/{}/{}".format(day, month, year)

        elif form == "us":
            return "{}/{}/{}".format(month, day, year)

        else:
            raise ValueError("'form' parameter must be one of 'exact', 'UK', 'US', 'long'")

def date_partial(prompt, unknown = True, na = True):
    """
    Gets input from the user for a date but some or all of the information can be unknown or not applicable

    PARAMETERS:
    - prompt (str): What to display before asking the user for input
    - unknown (bool): Whether or not to allow 'unknown' as an input
    - na (bool): Whether or not to allow 'n/a' as an input

    RETURNS:
    - date (str): The date in exact form (year-month-day)
    """

    print(prompt+"\n")

    year = int_range("Year: ", None, None, unknown, na)

    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    allowed = months
    allowed.extend(["1","2","3","4","5","6","7","8","9","10","11","12"])
    month = str_list("Month: ", allowed, True, unknown, na)
    if month in months:
        month = months.index(month) + 1
    elif month != "unknown" and month != "n/a":
        month = int(month)

    day = int_range("Day: ", 1, 31, unknown, na)

    return "{}-{}-{}".format(year, month, day)