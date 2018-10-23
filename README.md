# Validation by James Wilson
[GitHub](https://github.com/GingerNinja1892/Validation)

## Summary
Tools for validating inputs or variables according to customisable specifications detailing what format, datatype, etc. the value must be.

## Standard Use
Create a specification using the 'Spec' class or a descendant of it (all descendants start with 'Spec') and pass this to 'is_valid', 'assert_valid' or 'validate_input'

## Functions
To validate data

### is_valid
Returns whether or not a parameter is valid according to a specification

### assert_valid
Throws an assertion error if a parameter is not valid according to a specification

### validate_input
Repeatedly asks the user for input until their input is valid according to a specification

### true_false
A variant of 'validate_input', repeatedly asks the user for input until they input a boolean-like value and then converts it into this boolean value

### date
Gets the user to input a year, month and day

### time
Gets the user to input an hour, minute, second and optionally parts of a second

### datetime
Gets the user to input a year, month, day, hour, minute, second and optionally parts of a second

## Spec classes
Used for creating specifications for use in functions to validate

### Spec
Specifies the format of data in general

### SpecStr
Specifies the format of a string

### SpecNum
Specifies the format of a number

### SpecIntRange
Specifies the format of an integer in a range

### SpecIntList
Specifies the format of an integer from a list of allowed integers

### SpecFloatRange
Specifies the format of a float in a range

### SpecFloatList
Specifies the format of a float from a list of allowed floats