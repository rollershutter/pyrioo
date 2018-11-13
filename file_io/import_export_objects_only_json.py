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
# import pickle
from hashlib_tools.check_file import checksum_from_file_with, method_from  # , method_short
# _hashfile_from, checksum_from_file_with  #hashmethod_hashfile_from, checksum_from_file_with  # _checksum_from_file
from hashlib_tools.hashlib_tool import method_short

####
IO_DEBUG = False  # True


#   ## delegates read/write json/pickle
def read_json(file_name, json_object_hook):
    """
    Reads a json file with json module.
    Args:
        file_name: file to read obj from
    Return:
        <jsonified object>: json object representation
    """
    with open(file_name, 'r') as file_object:
        out = json.loads(file_object.read(), object_hook=json_object_hook)
        #print(out, type(out))
    return out


def write_json(obj_to_export, file_name, json_encoder):
    """
    Write json representation of object to file.
    Args:
        obj_to_export: object to export
        file_name: file to write obj to
        :param json_encoder: JSONEncoder class or None
    """
    with open(file_name, 'w') as file_object:
        file_object.write(json.dumps(obj_to_export, cls=json_encoder, sort_keys=True, indent=4))


##
#def import_obj_with(file_name, hash_method_str, d_import_func):
def import_obj_with(file_name, json_object_hook=None, method_str='sha256'):
    """Import a object from given file, checksum validation, optional json-decoding-method.
       calls read_json() -> json.loads()
       Args:
           file_name: file to load json-data from
           json_object_hook: optional decode-method to be passed to json.loads()
           method_str: short-method-name of desired hashlib-method, defaults to 'sha256'
       Returns:
           <json-repr/obj>: object of type provided with optional json_object_hook, json-representation otherwise
    """
    hash_file = _hashfile_from(file_name, method_from(method_str))
    try:
        hash_f = open(hash_file, 'r')
        my_hash = hash_f.read()
        if not my_hash.rstrip().endswith(checksum_from_file_with(file_name,
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


##
def export_obj_with(obj_to_export, file_name, json_encoder=None, method_str="sha256"):
    """Export a object to given file, checksum saving, optional JSONEncoder class.
       calls write_json() -> json.dumps()
       Args:
           obj_to_export: object to export,
                    has to be 'JSON serializable', otherwise a specialised JSONEncoder class is obligatory
           file_name: file to write json-data to
           json_encoder: optional JSONEncoder class
                    to be passed to json.dumps()
           method_str: short-method-name of desired hashlib-method,
                    defaults to 'sha256'
    """
    write_json(obj_to_export, file_name, json_encoder)
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
        hash_file_object.write(checksum_from_file_with(file_name, method_string))
    return True


#######################################################################################################################


def main(args):
    # testing module:
    # now import/export is json.loads/json.dumps only,
    #   with sha256 checksum by default,
    #   with optional JSONEncoder/decode-method
    from os import environ as os_environ

    # setting a file to save/load
    data_path = os_environ['PWD']
    file_name = '%s/py_json_tests_testobject.json' % data_path

    # define a custom class, providing conversion to dict for json-i/o:
    class MyObj2():
        #l = []
        next_id = 0

        def __init__(self, state):
            MyObj2.next_id += 1
            self.id = MyObj2.next_id
            self.state = state

        def __str__(self):
            return str(self.to_dict())

        def to_dict(self):
            return {'class': self.__class__.__name__,
                    'id': self.id,
                    'state': self.state}

        @staticmethod
        def from_dict(dct):
            if "class" in dct and dct['class'] == MyObj2.__name__:
                return MyObj2(dct['state'])
            return dct

    # provide a JSONEncoder using instance-method to_dict():
    class ComplexEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, MyObj2):
                return obj.to_dict()
            return json.JSONEncoder.default(self, obj)

    # testing export/(re-)import with two objects in a loop:
    object_list = [MyObj2(({"min": 33.33, "avg": 44.44}, 2, 4)),
                   MyObj2(({"min": 32.23, "avg": 35.53}, 3, 4)),
                   ]
    for c_obj in object_list:
        #export_obj_with(c_obj.to_dict(), file_name, None, 'sha256')
        export_obj_with(c_obj, file_name, ComplexEncoder)  # , 'sha256')

        #t_obj = MyObj2.from_dict(import_obj_with(file_name, None, 'sha256'))
        t_obj = import_obj_with(file_name, MyObj2.from_dict)  # , 'sha256')
        print("{}".format(t_obj), type(t_obj))  # print(out, type(out))


    ####
    # test_list = []


####
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
