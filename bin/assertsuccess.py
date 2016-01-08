#!/usr/bin/env python
# Written by: Brian "grep whisperer" Hom

import csv
import subprocess
import sys
import xml

# Formatting vars
COLOR_OFF = "\033[0m"
B_RED = "\033[1;31m"
B_GREEN = "\033[1;32m"
UB_YELLOW = "\033[4;93m"
# Number of characters in the message (inc. trail)
#   before displaying PASS/FAIL
MESSAGE_LENGTH = 100

def usage():
    print("""Usage:
    {0} <log_file> <assert_file(s)>""".format(sys.argv[0]))

def append_trail(string, string_length, trail_character='.'):
    """Add a trail to the end of the provided string up to the defined length.

    Keyword arguments:
    string -- string -- The string to have a trail appended to it
    trail_character -- string -- The character to append to the string
    string_length -- int -- The number of characters the string should contain.
        It will equate to (orig_string + trail) == string_length

    Returns: string"""

    while len(string) < string_length:
        string += trail_character

    return string

def get_pass_fail_message(has_passed):
    """Get a boolean and return a formatted string.

    Keyword arguments:
    has_passed -- boolean -- The object to check against

    Returns: string"""

    if has_passed:
        return "{0}{2}{1}".format(
            B_GREEN,
            COLOR_OFF,
            "PASS"
        )
    else:
        return "{0}{2}{1}".format(
            B_RED,
            COLOR_OFF,
            "FAIL"
        )

def is_string_in_file(inputString, file):
    """Uses grep to search through the specified file for the list of strings.

    Keyword arguments:
    inputString -- string -- A string to check for in the provided file
    file -- string -- The file to check against

    Returns: boolean
    """

    if len(inputString) < 1:
        return False
   
    try:
        # grep will throw an exception(return 1) if the string isn't found
        subprocess.check_output("grep " + '"' + inputString + '"' + " "  + file, shell=True)
        output = True
    except subprocess.CalledProcessError as e:
        output = False

    return output


def assert_test(log_file_path, assert_file_path):
    """Checks the provided log file
    to see if it contains the strings provided in the assert file

    Keyword arguments:
    log_file_path -- string -- The path to the log file
    assert_file_path -- string -- The path to the assert file"""

    try:
        with open(log_file_path) as log_file, \
             open(assert_file_path) as assert_file:
            # Close the log file
            #   because opening it was just validating
            #   that it can be opened for the `grep` command
            log_file.close()

            asserts = csv.reader(assert_file)

            # Skip the first line,
            #   which contains the column headers for readability
            next(asserts)

            # Check each test type
            for row in asserts:
                print("{0}Checking {2!r}{1}".format(
                    UB_YELLOW,
                    COLOR_OFF,
                    row[0]
                ))

                # Check each assert
                # Skip the first entry
                #   because it is just the call type for printing
                for check in row[1:]:
                    message = "Checking for {0!r}".format(check)
                    message = append_trail(message, MESSAGE_LENGTH)

                    search_output = is_string_in_file(check, log_file_path)

                    # Should return success as True/False
                    #   rather than do output here
                    print("{0}{1}".format(
                        message,
                        get_pass_fail_message(search_output)
                    ))
    except IOError as e:
        # File(s) could not be opened
        print("Operation failed: {0}{2}{1}".format(B_RED, COLOR_OFF, e))
        exit(2)

if __name__ == "__main__":
    # Needs a log_file, and at least 1 assert_file
    if len(sys.argv[1:]) < 2:
        usage()
        exit(1)

    log_file_path = sys.argv[1]
    assert_file_path = sys.argv[2]

    if (log_file_path == "" or
        assert_file_path == ""):
        usage()
        exit(1)
    assert_test(log_file_path, assert_file_path)
    
