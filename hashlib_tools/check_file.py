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
from hashlib_tools.hashlib_tool import _hash_method_from, hashmethod_short


####
def _hashfile_from(file_name, hash_method):
    ext = hashmethod_short(hash_method)
    #print("DEBUG: %s"% ext)
    name = '_'.join(file_name.split('.'))
    return '%s.%s' % (name, ext)

def hashmethod_hashfile_from(file_name, hash_method_string):
    hash_method = _hash_method_from(hash_method_string)
    file_name = _hashfile_from(file_name, hash_method) #'%s.%s' % ('_'.join(file_name.split('.')), str(hash_method.__name__)[8::]) #,hash_method.lower)
    return hash_method, file_name

def checksum_from_file(p_name, method):
    with open(p_name, 'rb') as fh:
        m = method()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        #fh.close()
        ##return m.hexdigest()
    return m.hexdigest()

def checksum_from_file_with(file_path, method_string):
    return checksum_from_file(file_path, _hash_method_from(method_string))


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
    from hashlib_tool import _hash_method_from, hashmethod_short
    sys.exit(main(sys.argv))
