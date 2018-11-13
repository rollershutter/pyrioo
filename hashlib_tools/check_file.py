#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  check_file.py
#  python 2.7 / 3.5 - tested
#
#  TODO: clean up my room,
#        hashlib -> hash-api: 
#                   -hashlib_tools.hash_file(file_name, hash_string)
#
#  author: sebastian rollershutter
##
import hashlib
from hashlib_tools import VerbosErr, method_from

fallback_message = "select_hashlib - _hash_method_from(method_string): " \
                   + "error\ncalled with: %s - fallback to: %s!"


def _checksum_from_file(file_name, method):
    """Calculates checksum from given file with given hashlib-method.
    Args:
        file_name (str): file-name to get checksum from
        method (hashlib-method): hashlib-method to get checksum of given file
    Returns:
        str: hash/checksum of given file in file_name as hexdigest-string
    """
    with open(file_name, 'rb') as fh:
        m = method()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def checksum_from_file_with(file_name, method_string):
    """Get hashlib-method from method_string and return checksum from given file.
    Args:
        file_name (str): file-name to get checksum from
        method_string (str): name of desired hashlib-method to get checksum of given file
    Returns:
        str: hash/checksum of given file in file_name as hexdigest-string
    """
    return _checksum_from_file(file_name, method_from(method_string))


#######################################################################################################################


#######################################################################################################################
#### testing when this module is being called directly
def main(args):
    print(dir(hashlib))

    # tests
    m_default = hashlib.md5
    m_sha256 = hashlib.sha256

    method_strings = ("wrong", "sha256", "MD5", None)
    expected_methods = (m_default, m_sha256, m_default, m_default)
    # print(zip(method_strings, expected_methods))

    print("\ntesting:\n{0}\nexpecting:\n{1}\n".format(method_strings, expected_methods))
    test_name = "blabla_blubb.pkl"
    for s, em in zip(method_strings, expected_methods):  # method_strings:
        m = method_from(s)
        print("s: {0}\n  hash-method: {1}".format(s, m))
        if not m == em:
            raise VerbosErr(m, "test failed: expected {0}, got {1}".format(em, m))
    print("tests passed successfully.")
    return 0


####
if __name__ == '__main__':
    import sys
    #from hashlib_tools.hashlib_tool import method_from  # , method_short
    from hashlib_tool import method_from  # , method_short

    sys.exit(main(sys.argv))
