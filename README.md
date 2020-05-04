# [Validation](https://github.com/jamesw1892/Validation) by [jamesw1892](https://github.com/jamesw1892)

## Summary
Tools for validating inputs or variables according to specifications detailing what format, datatype, etc. the data must be.

## Normal Use
Create a specification using the 'Spec' class or a descendant of it (all descendants start with 'Spec') and pass this to 'is_valid', 'validate_input' or 'assert_valid' as explained below

## Functions
The following only explains the purpose of the functions, docstrings attached to the functions themselves explain the parameters and returns in detail

### is_valid
Return whether or not a parameter is valid according to a specification and the validated parameter

### validate_input
Repeatedly ask the user for input until their input is valid according to a specification and return their validated input

### assert_valid
Throw an assertion error if a parameter is not valid according to a specification, otherwise return it

### true_false
Repeatedly ask the user for an input until they input a boolean-like value and return the boolean version

### date
Repeatedly ask the user for a year, month and day until they input valid values and return this in a defined format

### time
Repeatedly ask the user to input hours, minutes and seconds until they input valid values and return this in a defined format

### datetime
Repeatedly ask the user to input a year, month, day, hours, minutes and seconds until they input valid values and return this in a defined format

## Specifications
Used for creating specifications detailing the format the data is required in for use in functions to validate

### Spec
Specifies the format of data in general. Records the datatype of the data and whether or not to allow the absence of a value.

### SpecStr
Specifies the format of a string. Records the list of allowed strings, whether or not to lower the string before checking it and whether or not to allow the absence of a value.

### SpecNum
Specifies the format of a number. Records the number of digits to round the data to before checking it, whether or not to only allow integers and whether or not to allow the absence of a value.

### SpecNumRange
Specifies the format of a number in a range. Records the minimum and maximum valid values, the number of digits to round the data to before checking it, whether or not to only allow integers and whether or not to allow the absence of a value.

### SpecNumList
Specifies the format of a number from a list of allowed numbers. Records the list of allowed numbers, the number of digits to round the data to before checking it, whether or not to only allow integers and whether or not to allow the absence of a value.
