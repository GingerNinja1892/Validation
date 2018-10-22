"""
JMW's Validation Library
December 2017

This validates many types of inputs in various ways by calling on one of the following subroutines which are in the form (name - description (perameters)):
    1) int_range - an integer in a range of integers, can have no minimum or maximum (prompt [, minimum = False, maximum = False])
    2) int_array - an integer in an array of integers (prompt,array)
    3) float_range - a float in a range of floats, can have no minimum or maximum (prompt [, minimum = False, maximum = False])
    4) float_array - a float in an array of floats, can round to a set number of decimal places (prompt,array [, toround = False, num_digits = 0])
    5) str_array - a string in an array of strings, can lower the case of the characters (prompt,array [, lower = False])
    6) true_false - true or false-like statements only (prompt)
    7) files - checks that a file exists (name)
"""

#   1) int_range - an integer in a range of integers, can have no minimum or maximum (prompt [, minimum = False, maximum = False])
def int_range(prompt, minimum = None, maximum = None):

    error = "Must be a whole number"
    if minimum:
        error += ", minimum: " + str(minimum)
    if maximum:
        error += ", maximum: " + str(maximum)

    if minimum and maximum:

        acceptable = False
        while not acceptable:
            try:
                variable = int(input(prompt))
            except ValueError:
                print(error)
            else:
                if not minimum <= variable <= maximum:
                    print(error)
                else:
                    acceptable = True

    elif minimum and not maximum:

        acceptable = False
        while not acceptable:
            try:
                variable = int(input(prompt))
            except ValueError:
                print(error)
            else:
                if variable < minimum:
                    print(error)
                else:
                    acceptable = True

    elif not minimum and maximum:

        acceptable = False
        while not acceptable:
            try:
                variable = int(input(prompt))
            except ValueError:
                print(error)
            else:
                if variable > maximum:
                    print(error)
                else:
                    acceptable = True

    else:

        acceptable = False
        while not acceptable:
            try:
                variable = int(input(prompt))
            except ValueError:
                print(error)
            else:
                acceptable = True

    return(variable)

#   2) int_array - an integer in an array of integers (prompt,array)
def int_array(prompt, array):
    
    error = "Must be a whole number and one of the following: " + str(array).replace("[","").replace("]","")
    acceptable = False
    while not acceptable:
        try:
            variable = int(input(prompt))
        except ValueError:
            print(error)
        else:
            i = 0
            while i < len(array) and not acceptable:

                if variable == array[i]:
                    acceptable = True

                i += 1

            if not acceptable:
                print(error)
                
    return(variable)

#   3) float_range - a float in a range of floats, can have no minimum or maximum (prompt [, minimum = False, maximum = False])
def float_range(prompt, minimum = None, maximum = None):

    error = "Must be a number"
    if minimum:
        error += ", minimum: " + str(minimum)
    if maximum:
        error += ", maximum: " + str(maximum)

    if minimum and maximum:

        acceptable = False
        while not acceptable:
            try:
                variable = float(input(prompt))
            except ValueError:
                print(error)
            else:
                if not minimum <= variable <= maximum:
                    print(error)
                else:
                    acceptable = True

    elif minimum and not maximum:
        
        acceptable = False
        while not acceptable:
            try:
                variable = float(input(prompt))
            except ValueError:
                print(error)
            else:
                if variable < minimum:
                    print(error)
                else:
                    acceptable = True

    elif not minimum and maximum:

        acceptable = False
        while not acceptable:
            try:
                variable = float(input(prompt))
            except ValueError:
                print(error)
            else:
                if variable > maximum:
                    print(error)
                else:
                    acceptable = True

    else:

        acceptable = False
        while not acceptable:
            try:
                variable = float(input(prompt))
            except ValueError:
                print(error)
            else:
                acceptable = True

    return(variable)

#   4) float_array - a float in an array of floats, can round to a set number of decimal places (prompt,array [, toround = False, digits = 0])
def float_array(prompt, array, num_digits=None):
    
    error = "Must be a number and one of the following: " + str(array).replace("[","").replace("]","")
    acceptable = False

    while not acceptable:
        try:
            variable = float(input(prompt))
        except ValueError:
            print(error)
        else:
            i = 0
            while i < len(array) and not acceptable:

                if (num_digits == 0 and round(variable) == array[i]) or (num_digits and round(variable, num_digits) == array[i]) or variable == array[i]:
                    acceptable = True

                i += 1

            if not acceptable:
                print(error)
                
    return(variable)

#   5) str_array - a string in an array of strings, can lower the case of the characters (prompt,array [, lower = False])
def str_array(prompt, array, lower=True):
    
    error = "Must be one of the following: " + str(array).replace("[","").replace("]","").replace("'","")
    acceptable = False

    while not acceptable:

        variable = input(prompt)

        i = 0
        while i < len(array) and not acceptable:

            if (lower and variable.lower() == array[i]) or (not lower and variable == array[i]):
                acceptable = True
            
            i += 1

        if not acceptable:
            print(error)
            
    return(variable)

#   6) true_false - true or false-like statements only (prompt)
def true_false(prompt):
    
    error = "Must be one of the following: yes, y, true, t, no, n, false, f"
    acceptable = False

    while not acceptable:
        variable = input(prompt).lower()

        if variable == "yes" or variable == "y" or variable == "true" or variable == "t":
            variable = True
            acceptable = True

        elif variable == "no" or variable == "n" or variable == "false" or variable == "f":
            variable = False
            acceptable = True

        else:
            print(error)
                
    return(variable)

#   7) file - checks that a file exists (name)
def files(name):

    try:
        f = open(name,"r")
    except FileNotFoundError:
        ans = False
    else:
        ans = True
        f.close()

    return(ans)

def date(prompt, na=False):

    error = "Date must be in the format 'D/M/Y' where D, M and Y are numbers, D is between 1 and 31 and M is between 1 and 12"
    acceptable = False
    while not acceptable:
        variable = input(prompt).strip().upper()
        temp = variable.split("/")
        if na and variable == "N/A":                           #FOR NOW ONLYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
            acceptable = True

        try:
            if 1 <= int(temp[0]) <= 31 and 1 <= int(temp[1]) <= 12 and int(temp[2]):
                acceptable = True
        except ValueError:
            pass
        
        if not acceptable:
            print(error)
    
    return variable

if __name__ == "__main__":

    from JMWLibPresentation import spacing
    done = False
    
    while not done:
        
        spacing()
        menu = int_range("MENU:\n1: An integer in a range of integers, can have minimum or maximum\n2: An integer in an array of integers\n3: A float in a range of floats, can have minimum or maximum\n4: A float in an array of floats, can round to a set number of decimal places\n5: A string in an array of strings, can lower the case of the characters\n6: True or false statements only\n7: Check that a file exists\n8: Exit\nInput the number between 1 and 8 corresponding to the option you wish to select: ",1,8)

        if menu == 8:
            done = True
            
        else:
            spacing()
            
            if menu == 1:

                havemin = true_false("Do you want a minimum? ")
                havemax = true_false("Do you want a maximum? ")

                if havemin and havemax:
                    minimum = int_range("Minimum: ")
                    maximum = int_range("Maximum: ")
                    ans = int_range("Input: ",minimum,maximum)
                elif havemin and not havemax:
                    minimum = int_range("Minimum: ")
                    ans = int_range("Input: ",minimum)
                elif not havemin and havemax:
                    maximum = int_range("Maximum: ")
                    ans = int_range("Input: ",False,maximum)
                else:
                    ans = int_range("Input: ")

            elif menu == 2:
                
                num = int_range("Number of accepted integers: ",1)
                array = []
                for i in range(num):
                    array.append(int_range("Accepted integer "+str(i+1)+": "))
                ans = int_array("Input: ",array)

            elif menu == 3:

                havemin = true_false("Do you want a minimum? ")
                havemax = true_false("Do you want a maximum? ")

                if havemin and havemax:
                    minimum = float_range("Minimum: ")
                    maximum = float_range("Maximum: ")
                    ans = float_range("Input: ",minimum,maximum)
                elif havemin and not havemax:
                    minimum = float_range("Minimum: ")
                    ans = float_range("Input: ",minimum)
                elif not havemin and havemax:
                    maximum = float_range("Maximum: ")
                    ans = float_range("Input: ",False,maximum)
                else:
                    ans = float_range("Input: ")

            elif menu == 4:
                
                num = int_range("Number of accepted floating points: ",1)
                array = []
                for i in range(num):
                    array.append(float_range("Accepted float "+str(i+1)+": "))
                toround = true_false("Would you like the inputted string to be rounded before being compared? ")
                if toround == True:
                    digits = int_range("Number of digits after the decimal place to round to (can be negative, if you don't want to round, it doesn't matter what you enter): ")
                else:
                    digits == False
                ans = float_array("Input: ",array,digits)

            elif menu == 5:
                
                num = int_range("Number of accepted strings: ",1)
                array = []
                for i in range(num):
                    array.append(input("Accepted string "+str(i+1)+": "))
                lower = true_false("Would you like the inputted string to be lowered to lower case before being compared? ")
                ans = str_array("Input: ",array,lower)

            elif menu == 6:
                
                ans = true_false("Input: ")

            else:

                ans = files(input("File name with extension: "))
                
            print("Success, you entered",ans)
            input("Press ENTER to continue: ")