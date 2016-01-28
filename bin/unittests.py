#!/usr/bin/env python

"""Usage: python bin/unittests.py
Adding option '-v' will run in verbose-mode which will show each test running individually."""

import unittest

import assertsuccess

class Files(unittest.TestCase):
    # (string, file, known_result)
    is_string_in_file_known_values = (
        (
            "foobar",
            "inbound/holiday/functional/inbound_holiday_voicemail_base.txt",
            False
        ),
    )

    def test_is_string_in_file(self):
        """is_string_in_file should give known result with known input"""

        for string, f, known_result in self.is_string_in_file_known_values:
            result = assertsuccess.is_string_in_file(string, f)

            self.assertEqual(known_result, result)

class String(unittest.TestCase):
    # (string, trail_chars, length, known_result)
    append_trail_to_string_known_values = (
        ("Foobar", ' ', 10, "Foobar    "),
        ("Foobar", '.', 10, "Foobar...."),
        (" Foobar", ' ', 10, " Foobar   "),
        (" Foobar ", '-', 10, " Foobar --"),
        ("  Foobar ", '.-', 15, "  Foobar .-.-.-"),
        (" bar Foo ", ' .', 4, " bar Foo "),
        (" Foobar ", '*+', 9, " Foobar *"),
        ("  Foobar ", '_', 50, "  Foobar _________________________________________"),
        (" Foo_bar ", '_!', 22, " Foo_bar _!_!_!_!_!_!_"),
        (" bar  Foo san", 'san', 17, " bar  Foo sansans"),
        ("Foobar", '', 20, "Foobar"),
        ("", '', 10, ""),
        ("", '.', 10, ".........."),
    )

    # (input_value, known_result)
    get_pass_fail_message_known_values = (
        (False, "\033[1;31mFAIL\033[0m"),
        (0, "\033[1;31mFAIL\033[0m"),
        (True, "\033[1;32mPASS\033[0m"),
        (1, "\033[1;32mPASS\033[0m"),
        (-1, "\033[1;32mPASS\033[0m"),
        ('0', "\033[1;32mPASS\033[0m"),
        ('1', "\033[1;32mPASS\033[0m"),
        ("Foobar", "\033[1;32mPASS\033[0m"),
    )

    def test_append_trail_to_string(self):
        """test_append_trail_to_string should give known result with known input"""
        
        for orig_string, \
            trail_chars, \
            string_length, \
            known_result in self.append_trail_to_string_known_values:
            result = assertsuccess.append_trail_to_string(orig_string,
                                                          trail_chars,
                                                          string_length)

            self.assertEqual(known_result, result)

    def test_get_pass_fail_message(self):
        """get_pass_fail_message should give known result with known input"""

        for value, known_result in self.get_pass_fail_message_known_values:
            result = assertsuccess.get_pass_fail_message(value)

            self.assertEqual(known_result, result)

if __name__ == '__main__':
    unittest.main()

    sys.exit(0)
