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
    {0} <log_file> <positive_assert_file> <negative_assert_file> <base_log_file>""".format(sys.argv[0]))

def append_trail_to_string(string, trail_string='.', string_length=100):
    """Add a trail to the end of the provided string up to the defined length.

    Keyword arguments:
    string -- string -- The string to have a trail appended to it
    trail_string -- string -- The characters to append to the string
    string_length -- int -- The number of characters the string should contain.
        It will equate to (orig_string + trail) == string_length

    Returns: string"""

    if (trail_string == '' or
        len(string) >= string_length):
        return string

    while len(string) < string_length:
        for char in trail_string:
            if len(string) >= string_length:
                break

            string = "".join([string, char])

    return string

def get_pass_fail_message(has_passed):
    """Get a boolean and return a formatted string.

    Keyword arguments:
    has_passed -- boolean -- The object to check against

    Returns: string"""

    status_message = ""
    output_color = ""

    if has_passed:
        output_color = B_GREEN
        status_message = "PASS"
    else:
        output_color = B_RED
        status_message = "FAIL"

    formatted_message = "".join([output_color, status_message, COLOR_OFF])

    return formatted_message

def is_string_in_file(string, file_path):
    """Searches a file if the provided string exists.
    
    Keyword arguments:
    string -- string -- The phrase to search for
    file_path -- string -- The file to check

    Returns: boolean"""

    try:
        string_in_file = False

        with open(file_path) as file:
            # Using mmap offers better memory performance
            #   especially for large files compared to using something like
            #   if string in open(file_path).read()
            buf = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
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
            buf = mmap.mmap(f.fileno(), 0)
            readline = buf.readline
            while readline():
                lines += 1

        return lines
    except IOError as e:
        # File(s) could not be opened
        print("Operation failed: {0}{2}{1}".format(B_RED, COLOR_OFF, e))
        exit(1)

def assert_test(log_file_path, assert_file_path, words_validate=True):
    """Checks the provided log file
    to see if it contains the strings provided in the assert file

    Keyword arguments:
    log_file_path -- string -- The path to the log file
    assert_file_path -- string -- The path to the assert file
    words_validate -- bool -- When True, check if words exist for PASS.
        If False, then check if words exist for FAIL."""

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
                # Skip row if there is not at least a test type and assertion
                if len(row) < 2:
                    continue

                # Output checking test type
                print("{0}Checking '{2}'{1}".format(
                    UB_YELLOW,
                    COLOR_OFF,
                    row[0]
                ))

                # Check each assert
                # Skip the first entry
                #   because it is just the call type for printing
                for words in row[1:]:
                    # Skip if entry is empty
                    if words.strip() == "":
                        continue

                    if words_validate:
                        message = "Checking for '{0}'".format(words)
                        search_result = is_string_in_file(words, log_file_path)
                    else:
                        message = "Verifying there are no '{0}' messages".format(words)
                        search_result = not is_string_in_file(words, log_file_path)
                    message = append_trail_to_string(message, '.', MESSAGE_LENGTH)

                    # This formats to something like:
                    #   Checking for 'TEST'.....[PASS]
                    message = "".join([message, '[', get_pass_fail_message(search_result), ']'])
                    # Should return success as True/False
                    #   rather than do output here
                    print(message)
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

def main(log_file_path,
         positive_assert_file_path,
         negative_assert_file_path,
         base_log_file_path):
    """Run the assertion files checks against the log file.

    Keyword arguments:
    log_file_path -- string -- The log to check against
    positive_assert_file_path -- string -- CSV file with strings to check the log file for having to pass
    negative_assert_file_path -- string -- CSV file with strings to check the log file for NOT having to pass
    base_log_file_path -- string -- The control log file which has a known working case"""

    log_file_path = log_file_path.strip()
    positive_assert_file_path = positive_assert_file_path.strip()
    negative_assert_file_path = negative_assert_file_path.strip()
    base_log_file_path = base_log_file_path.strip()

    if (not log_file_path or
        not positive_assert_file_path or
        not negative_assert_file_path or
        not base_log_file_path):
        usage()
        exit(1)

    # Dividing line in output
    dividing_line = append_trail_to_string("", '-', MESSAGE_LENGTH)

    assert_test(log_file_path, positive_assert_file_path, True)

    print(dividing_line)

    message = "Checking line count against base"
    message = append_trail_to_string(message, '.', MESSAGE_LENGTH)
    log_size_equal = assert_log_size(log_file_path, base_log_file_path)
    message = "".join([message, '[', get_pass_fail_message(log_size_equal), ']'])
    print(message)

    print(dividing_line)

    assert_test(log_file_path, negative_assert_file_path, False)

    # Everything ran without a problem
    return True

if __name__ == '__main__':
    # Needs a log_file,
    # a positive assertion file,
    # a negative assertion file,
    # and a base_log_file
    if len(sys.argv[1:]) < 4:
        usage()
        exit(1)

    log_file_path = sys.argv[1]
    positive_assert_file_path = sys.argv[2]
    negative_assert_file_path = sys.argv[3]
    base_log_file_path = sys.argv[4]

    main(log_file_path, positive_assert_file_path, negative_assert_file_path, base_log_file_path)
