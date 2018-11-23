#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#  import_export_objects_only_json.py
#  python 2.7 / 3.5 - tested
#
#  author: sebastian rollershutter
##
import json
from hashlib_tools import from_file_with, method_from, method_short


####
IO_DEBUG = False  # True
SORT_KEYS, INDENT = True, 4

#   ## read/write json
def read_json(file_name, json_object_hook):
    """Reads a json file with json module.
    Args:
        :param file_name: file to read obj from
        :param json_object_hook: decode-method (json-dict-conversion)
    Return:
        :return <jsonified object>: json object representation
    """
    with open(file_name, 'r') as file_object:
        out = json.loads(file_object.read(), object_hook=json_object_hook)
        #print(out, type(out))
    return out


def write_json(obj_to_export, file_name, json_encoder):  # , sort_keys=True, indent=4):
    """Write json representation of object to file.
    Args:
        :param obj_to_export: object to export
        :param file_name: file to write obj to
        :param json_encoder: JSONEncoder class or None
    """
    with open(file_name, 'w') as file_object:
        file_object.write(json.dumps(obj_to_export, cls=json_encoder, sort_keys=SORT_KEYS, indent=INDENT))


#   ## import/export
def import_obj_with(file_name, json_object_hook=None, method_str='sha256'):
    """Import a object from given file, checksum validation, optional json-decoding-method.
       calls read_json() -> json.loads()
       Args:
           :param file_name: file to load json-data from
           :param json_object_hook: optional decode-method to be passed to json.loads()
           :param method_str: short-method-name of desired hashlib-method, defaults to 'sha256'
       Returns:
           :return <json-repr/obj>: object of type provided with optional json_object_hook, json-representation otherwise
    """
    hash_file = _hashfile_from(file_name, method_from(method_str))
    try:
        hash_f = open(hash_file, 'r')
        my_hash = hash_f.read()
        if not my_hash.rstrip().endswith(from_file_with(file_name,
                                                        method_str)):  # python3: checksum_from_file().encode() returns bytestring - removed encode
            if IO_DEBUG:
                print('checksum not correct!')
            return
        ##
        if IO_DEBUG:
            print('checksum correct! -> importing')
        try:
            loaded_obj = read_json(file_name, json_object_hook)
            return loaded_obj
        #except FileNotFoundError:
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


def export_obj_with(obj_to_export, file_name, json_encoder=None, method_str="sha256"):
    """Export a object to given file, checksum saving, optional JSONEncoder class.
       calls write_json() -> json.dumps()
       Args:
           :param obj_to_export: object to export,
                    has to be 'JSON serializable', otherwise a specialised JSONEncoder class is obligatory
           :param file_name: file to write json-data to
           :param json_encoder: optional JSONEncoder class
                    to be passed to json.dumps()
           :param method_str: short-method-name of desired hashlib-method,
                    defaults to 'sha256'
    """
    write_json(obj_to_export, file_name, json_encoder)
    # if save_checksum_from_file_with(file_name, method_str):
    #    return True
    save_checksum_from_file_with(file_name, method_str)


#   ## checksum-file
def _hashfile_from(file_name, hash_method):
    """Construct a hash/checksum-file-name from the given file-name and the given hashlib.hash-method short-name.
    Get a files file-name string and a hashlib.hash-method shortname and return a filename string.
    Args:
        :param file_name (str):
        :param hash_method (hashlib.[method]): hashlib hash-method e.g: hashlib.md5
    Returns:
        :return str: hash-file name to save checksum of file given in file_name.
    """
    ext = method_short(hash_method)
    # print("DEBUG: %s"% ext)
    name = '_'.join(file_name.split('.'))
    return '%s.%s' % (name, ext)


def save_checksum_from_file_with(file_name, method_string):
    """Get hashlib-method from method_string and save checksum of given file to appropriate checksum-file.
    Args:
        :param file_name (str): file-name to get checksum from
        :param method_string (str): name of desired hashlib-method to get checksum of given file
    Returns:
        :return bool: True if checksum written to file
    """
    hash_file_name = _hashfile_from(file_name, method_from(method_string))

    with open(hash_file_name, 'w') as hash_file_object:
        ##print >> hash_file_object, checksum_from_file(file_path, hash_method)			## python2.7
        ##print(checksum_from_file(file_path, hash_method), file=hash_file_object)		## python3.5
        hash_file_object.write(from_file_with(file_name, method_string))
    return True
