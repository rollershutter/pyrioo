#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hashlib_tool.py
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


####
def hashmethod_short(hash_method):
    return hash_method.__name__[8::].lower()

def _hash_method_from(method_string):
    fallback_method = hashlib.md5
    try:
        hash_method = getattr(hashlib, method_string.lower())
    except: # (AttributeError, TypeError):
        print(fallback_message % (method_string, hashmethod_short(fallback_method)))
        hash_method = fallback_method
    #except TypeError:
    #   hash_method = fallback_method
    #print("DEBUG:", dir(hash_method), hash_method.__name__[8::]) #.__str__())
    return hash_method


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
    for s, em in zip(method_strings, expected_methods): #method_strings:
        m = _hash_method_from(s)
        print( "s: {0}\n  hash-method: {1}".format(s, m) )
        if not m == em:
            raise VerbosErr(m, "test failed: expected {0}, got {1}".format(em, m))
    print("tests passed successfully.")
    return 0

####
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))