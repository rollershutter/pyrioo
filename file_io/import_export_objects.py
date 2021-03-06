#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#  import_export_objects.py
#  python 2.7 / 3.5 - tested
#
#  TODO: delegation - func injection - done
#        outsourcing check_file to hashlib_tools-module for saving
#          objects - done
#
#  author: sebastian rollershutter
##
import json
import pickle
from hashlib_tools.checksum import from_file_with, method_from  # , method_short
# _hashfile_from, checksum_from_file_with  #hashmethod_hashfile_from, checksum_from_file_with  # _checksum_from_file
from hashlib_tools.method_tool import method_short

####
IO_DEBUG = False  # True


## delegates read/write json/pickle
def read_pickle(file_name):
    """
    Reads a pickled file with pickle module.
    Args:
        file_name: file to read obj from
    Return:
        <pickled object>: object from pickled file
    """
    with open(file_name, 'rb') as file_object_b:
        out = pickle.load(file_object_b)
    return out


def read_json(file_name):
    """
    Reads a json file with json module.
    Args:
        file_name: file to read obj from
    Return:
        <jsonified object>: json object representation
    """
    with open(file_name, 'r') as file_object:
        out = json.loads(file_object.read())
        print(out, type(out))
    return out


def write_pickle(obj_to_export, file_name):
    """
    Serialize given obj in obj_to_export to file given in file_path.
    Args:
        obj_to_export: object to export
        file_name: file to write obj to
    """
    prot = 0
    with open(file_name, 'wb') as file_object:
        pickle.dump(obj_to_export, file_object, prot)


def write_json(obj_to_export, file_name):
    """
    Write json representation of object to file.
    Args:
        obj_to_export: object to export
        file_name: file to write obj to
    """
    with open(file_name, 'w') as file_object:
        file_object.write(json.dumps(obj_to_export))


##
def import_obj_with(file_name, hash_method_str, d_import_func):
    hash_file = _hashfile_from(file_name, method_from(hash_method_str))
    try:
        hash_f = open(hash_file, 'r')
        my_hash = hash_f.read()
        if not my_hash.rstrip().endswith(from_file_with(file_name,
                                                        hash_method_str)):  # python3: checksum_from_file().encode() returns bytestring - removed encode
            if IO_DEBUG:
                print('checksum not correct!')
            return
        ##
        if IO_DEBUG:
            print('checksum correct! -> importing')
        try:
            loaded_obj = d_import_func(file_name)
            return loaded_obj
        #except FileNotFoundError:  # TODO: include a FileNotFoundErr...
        #    if IO_DEBUG:
        #        print('file: %s not found...' % file_name)
        except Exception as ex:
            print("{}".format(ex))
    # except TypeError:
    #	byte needed, not string
    # except Error as err:
    #	print("{}".format(err))
    except IOError:
        if IO_DEBUG:
            print('no hash-file found...')


##
def export_obj_with(obj_to_export, file_name, method_str, d_export_func):
    d_export_func(obj_to_export, file_name)
    # if save_checksum_from_file_with(file_name, method_str):
    #    return True
    save_checksum_from_file_with(file_name, method_str)


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
    """Get hashlib-method from method_string and save checksum of given file to appropriate checksum-file.
    Args:
        file_name (str): file-name to get checksum from
        method_string (str): name of desired hashlib-method to get checksum of given file
    Returns:
        bool: True if checksum written to file
    """
    hash_file_name = _hashfile_from(file_name, method_from(method_string))

    with open(hash_file_name, 'w') as hash_file_object:
        ##print >> hash_file_object, checksum_from_file(file_path, hash_method)			## python2.7
        ##print(checksum_from_file(file_path, hash_method), file=hash_file_object)		## python3.5
        hash_file_object.write(from_file_with(file_name, method_string))
    return True


def export_obj_with(obj_to_export, file_name, method_str, d_export_func):
    d_export_func(obj_to_export, file_name)
    # if save_checksum_from_file_with(file_name, method_str):
    #    return True
    save_checksum_from_file_with(file_name, method_str)
