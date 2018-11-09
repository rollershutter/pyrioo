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
#  Copyright 2018 sebastian rollershutter
##
import hashlib
fallback_message = "select_hashlib - _hash_method_from(method_string): " \
                 + "error\ncalled with: %s - fallback to: %s!"
from hashlib_tools.error_classes import VerbosErr
from hashlib_tools.hashlib_tool import _method_from, method_short


####
def _hashfile_from(file_name, hash_method):
    """Construct a hash/checksum-file-name from the given file-name and the given hashlib.hash-method short-name.
    Get a files file-name string and a hashlib.hash-method shortname and return a filename string.
    Args:
        file_name (str):
        hash_method (hashlib.[method]): hashlib hash-method e.g: hashlib.md5
    Returns:
        str: hash-file name to save checksum of file given in file_name.
    """
    ext = method_short(hash_method)
    #print("DEBUG: %s"% ext)
    name = '_'.join(file_name.split('.'))
    return '%s.%s' % (name, ext)


def hashmethod_hashfile_from(file_name, hash_method_string):
    #"""
    #
    #:param file_name:
    #:param hash_method_string:
    #:return:
    #"""
    """

    Args:
        file_name (str): file-name of file to get a checksum from.
        hash_method_string (str): hash-method short-name string to get a hashlib-hash-method
    Returns:
        hashlib hash-method: hash-method to use for hashing given file in file_name
        str: file-name to save the checksum of given file in file_name
    """
    hash_method = _method_from(hash_method_string)
    file_name = _hashfile_from(file_name, hash_method) #'%s.%s' % ('_'.join(file_name.split('.')), str(hash_method.__name__)[8::]) #,hash_method.lower)
    return hash_method, file_name


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
        #fh.close()
        ##return m.hexdigest()
    return m.hexdigest()


def checksum_from_file_with(file_name, method_string):
    """Get hashlib-method from method_string and return checksum from given file.
    Args:
        file_name (str): file-name to get checksum from
        method_string (str): name of desired hashlib-method to get checksum of given file
    Returns:
        str: hash/checksum of given file in file_name as hexdigest-string
    """
    return _checksum_from_file(file_name, _method_from(method_string))

def save_checksum_from_file_with(file_name, method_string):
    """Get hashlib-method from method_string and return checksum from given file.
    Args:
        file_name (str): file-name to get checksum from
        method_string (str): name of desired hashlib-method to get checksum of given file
    Returns:
        str: hash/checksum of given file in file_name as hexdigest-string
    """
    return _checksum_from_file(file_name, _method_from(method_string))


#######################################################################
#### testing when this module is being called directly
def main(args):
    print(dir(hashlib))

    #tests
    m_default = hashlib.md5
    m_sha256 = hashlib.sha256

    method_strings = ("wrong", "sha256", "MD5", None)
    expected_methods = (m_default, m_sha256, m_default, m_default)
    #print(zip(method_strings, expected_methods))

    print("\ntesting:\n{0}\nexpecting:\n{1}\n".format(method_strings,expected_methods))
    test_name = "blabla_blubb.pkl"
    for s, em in zip(method_strings, expected_methods): #method_strings:
        m, f = hashmethod_hashfile_from(test_name, s)
        print( "s: {0}\n  hash-method: {2}\n  hash-file: {1}".format(s, f, m) )
        if not m == em:
            raise VerbosErr(m, "test failed: expected {0}, got {1}".format(em, m))
    print("tests passed successfully.")
    return 0

####
if __name__ == '__main__':
    import sys
    from hashlib_tools.hashlib_tool import _method_from, method_short
    sys.exit(main(sys.argv))
