# [Validation](https://github.com/GingerNinja1892/Validation) by James Wilson AKA [GingerNinja1892](https://github.com/GingerNinja1892)

## Summary
Tools for validating inputs or variables according to specifications detailing what format, datatype, etc. the value must be.

## Normal Use
Create a specification using the 'Spec' class or a descendant of it (all descendants start with 'Spec') and pass this to 'is_valid', 'assert_valid' or 'validate_input'

## Functionality
* __is_valid__: returns whether or not a parameter is valid according to a specification
* __assert_valid__: Throws an assertion error if a parameter is not valid according to a specification
* __validate_input__: Repeatedly asks the user for input until their input is valid according to a specification
* __true_false__: A variant of 'validate_input', repeatedly asks the user for input until they input a boolean-like value and then converts it into this boolean value
* __date__: Gets the user to input a year, month and day
* __time__: Gets the user to input an hour, minute, second and optionally parts of a second
* __datetime__: Gets the user to input a year, month, day, hour, minute, second and optionally parts of a second

## Spec classes
Used for creating specifications for use in functions to validate

* __Spec__: Specifies the format of data in general
* __SpecStr__: Specifies the format of a string
* __SpecNum__: Specifies the format of a number
* __SpecIntRange__: Specifies the format of an integer in a range
* __SpecIntList__: Specifies the format of an integer from a list of allowed integers
* __SpecFloatRange__: Specifies the format of a float in a range
* __SpecFloatList__: Specifies the format of a float from a list of allowed floats