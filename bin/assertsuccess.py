#!/usr/bin/env python
# Written by: Brian "grep whisperer" Hom

import csv
import sys
import mmap
import os.path

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
    {0} <log_file> <assert_file> <base_log_file>""".format(sys.argv[0]))

def append_trail_to_string(string, trail_character='.', string_length=100):
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

def is_string_in_file(string, file_path):
    """Searches a file if the provided string exists.
    
    Keyword arguments:
    string -- string -- The phrase to search for
    file -- string -- The file to check

    Returns: boolean"""

    try:
        string_in_file = False

        with open(file_path) as file:
            # Using mmap offers better memory performance
            #   especially for large files compared to using something like
            #   if string in open(file_path).read()
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as buf:
                # string must be converted to a bytes object
                #   for it to be usable with the mmap object
                bytes_string = bytes(string)

                string_in_file = buf.find(bytes_string) != -1

        return string_in_file
    except IOError as e:
        # File(s) could not be opened
        print("Operation failed: {0}{2}{1}".format(B_RED, COLOR_OFF, e))
        exit(1)

def count_lines_in_file(file_path):
    """Check the number of lines in a file

    Keyword arguments:
    file_path -- string -- The path to the log file

    Returns: int"""
    try:
        lines = 0

        with open(file_path, "r+") as f:
            with mmap.mmap(f.fileno(), 0) as buf:
                readline = buf.readline
                while readline():
                    lines += 1

        return lines
    except IOError as e:
        # File(s) could not be opened
        print("Operation failed: {0}{2}{1}".format(B_RED, COLOR_OFF, e))
        exit(1)

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
            #   that it can be opened
            log_file.close()

            asserts = csv.reader(assert_file)

            # Skip the first line,
            #   which contains the column headers for readability
            next(asserts)

            # Check each test type
            for row in asserts:
                print("{0}Checking '{2}'{1}".format(
                    UB_YELLOW,
                    COLOR_OFF,
                    row[0]
                ))

                # Check each assert
                # Skip the first entry
                #   because it is just the call type for printing
                for check in row[1:]:
                    message = "Checking for '{0}'".format(check)
                    message = append_trail_to_string(message, '.', MESSAGE_LENGTH)

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
        exit(1)

def assert_log_size(log_file_path, base_log_file_path):
    """Checks the provided log file to see if it contains the same number 
    of lines as a known good log(base_log_file_path) 

    Keyword arguments:
    log_file_path -- string -- The path to the log file
    base_log_file_path -- string -- The path to the base log file"""

    log_lines = count_lines_in_file(log_file_path)
    base_lines = count_lines_in_file(base_log_file_path)

    line_counts_equal = log_lines == base_lines

    return line_counts_equal

def assert_negative_test(log_file_path):
    """Checks the provided log file to see if it does NOT contain certain words 

    Keyword arguments:
    log_file_path -- string -- The path to the log file"""

    try:
        bad_words = [
                        "NOTICE",
                        "notice",
                        "WARNING",
                        "warning",
                        "ERROR",
                        "error",
                        "DEBUG",
                        "debug",
                    ]

        for word in bad_words:
            message = "Verifying there are no '{0}' messages".format(word)
            message = append_trail_to_string(message, '.', MESSAGE_LENGTH)
            search_output = is_string_in_file(word, log_file_path)
            print("{0}{1}".format(
                message,
                get_pass_fail_message(not search_output)
            ))

    except IOError as e:
        # File(s) could not be opened
        print("Operation failed: {0}{2}{1}".format(B_RED, COLOR_OFF, e))
        exit(1)

def main(log_file_path, assert_file_path, base_log_file_path):
    log_file_path = log_file_path.strip()
    assert_file_path = assert_file_path.strip()
    base_log_file_path = base_log_file_path.strip()

    if (not log_file_path or
        not assert_file_path or
        not base_log_file_path):
        usage()
        exit(1)

    # Dividing line in output
    dividing_line = append_trail_to_string("", '-', MESSAGE_LENGTH)

    assert_test(log_file_path, assert_file_path)

    print(dividing_line)

    message = "Checking line count against base"
    message = append_trail_to_string(message, MESSAGE_LENGTH)
    log_size_equal = assert_log_size(log_file_path, base_log_file_path)
    print("{0}{1}".format(
        message,
        get_pass_fail_message(log_size_equal)
    ))

    print(dividing_line)

    assert_negative_test(log_file_path)

if __name__ == '__main__':
    # Needs a log_file, an assertion file, and a base_log_file
    if len(sys.argv[1:]) < 3:
        usage()
        exit(1)

    log_file_path = sys.argv[1]
    assert_file_path = sys.argv[2]
    base_log_file_path = sys.argv[3]

    main(log_file_path, assert_file_path, base_log_file_path)
