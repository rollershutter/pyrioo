#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#  pickle_obj_python3_1a
#  python 2.7 / 3.5 - tested
#
#  TODO: delegation - func injection - done
#        outsourcing check_file to hashlib_tools-module for saving
#          objects - done
#
#  Copyright 2018 sebastian rollershutter
##
import json
import pickle
from hashlib_tools.check_file import checksum_from_file_with, _method_from  #, method_short
# _hashfile_from, checksum_from_file_with  #hashmethod_hashfile_from, checksum_from_file_with  # _checksum_from_file
from hashlib_tools.hashlib_tool import method_short


####
IO_DEBUG = False  # True


## delegates read/write json/pickle
def read_pickle(file_name):
    with open(file_name, 'rb') as file_object_b:
        out = pickle.load(file_object_b)
    return out


def read_json(file_name):
    with open(file_name, 'r') as file_object:
        out = json.loads(file_object.read())
    return out


def write_pickle(obj_to_export, file_path):
    prot = 0
    with open(file_path, 'wb') as file_object:
        pickle.dump(obj_to_export, file_object, prot)


def write_json(obj_to_export, file_path):
    with open(file_path, 'w') as file_object:
        file_object.write(json.dumps(obj_to_export))


##
def import_obj_with(file_path, hash_method_str, d_import_func):
    hash_file = _hashfile_from(file_path, _method_from(hash_method_str))
    try:
        hash_f = open(hash_file, 'r')
        my_hash = hash_f.read()
        if not my_hash.rstrip().endswith(checksum_from_file_with(file_path, hash_method_str)):  # python3: checksum_from_file().encode() returns bytestring - removed encode
            if IO_DEBUG:
                print('checksum not correct!')
            return
        ##
        if IO_DEBUG:
            print('checksum correct! -> importing')
        try:
            loaded_obj = d_import_func(file_path)
            return loaded_obj
        except FileNotFoundError:
            if IO_DEBUG:
                print('file: %s not found...' % file_path)
    # except TypeError:
    #	byte needed, not string
    # except Error as err:
    #	print("{}".format(err))
    except IOError:
        if IO_DEBUG:
            print('no hash-file found...')


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
    # print("DEBUG: %s"% ext)
    name = '_'.join(file_name.split('.'))
    return '%s.%s' % (name, ext)


def save_checksum_from_file_with(file_name, method_string):
    """Get hashlib-method from method_string and return checksum from given file.
    Args:
        file_name (str): file-name to get checksum from
        method_string (str): name of desired hashlib-method to get checksum of given file
    Returns:
        str: hash/checksum of given file in file_name as hexdigest-string
    """
    hash_file_name = _hashfile_from(file_name, _method_from(method_string))

    with open(hash_file_name, 'w') as hash_file_object:
        ##print >> hash_file_object, checksum_from_file(file_path, hash_method)			## python2.7
        ##print(checksum_from_file(file_path, hash_method), file=hash_file_object)		## python3.5
        hash_file_object.write(checksum_from_file_with(file_name, method_string))


def export_obj_with(obj_to_export, file_name, method_str, d_export_func):
    d_export_func(obj_to_export, file_name)
    save_checksum_from_file_with(file_name, method_str)
    return True
