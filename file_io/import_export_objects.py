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
from hashlib_tools.check_file import hashmethod_hashfile_from, checksum_from_file


####
## delegate
def read_pickle(file_name):
    with open(file_name, 'rb') as file_object_b:
        out = pickle.load(file_object_b)
    return out

## delegate
def read_json(file_name):
    with open(file_name, 'r') as file_object:
        out = json.loads(file_object.read())
    return out

##
def import_obj_with(file_path, hash_method, d_import_func):
    hash_method, hash_file = hashmethod_hashfile_from(file_path, hash_method)
    try:
        hash_f = open(hash_file, 'r')
        my_hash = hash_f.read()
        if not my_hash.rstrip().endswith(checksum_from_file(file_path,
                                                            hash_method)):  ## python3: checksum_from_file().encode() returns bytestring - removed encode
            print('checksum not correct!')
            return
        ##
        print('checksum correct! -> importing')
        try:
            loaded_obj = d_import_func(file_path)
            return loaded_obj
        except FileNotFoundError:
            print('file: %s not found...' % file_path)
    # except TypeError:
    #	byte needed, not string
    # except Error as err:
    #	print("{}".format(err))
    except IOError:
        print('no hash-file found...')

def write_pickle(obj_to_export, file_path):
    prot = 0
    with open(file_path, 'wb') as file_object:
        pickle.dump(obj_to_export, file_object, prot)

def write_json(obj_to_export, file_path):
    with open(file_path, 'w') as file_object:
        file_object.write(json.dumps(obj_to_export))

def export_obj_with(obj_to_export, file_path, hash_method, d_export_func):
    d_export_func(obj_to_export, file_path)
    hash_method, hash_file_name = hashmethod_hashfile_from(file_path, hash_method)

    with open(hash_file_name, 'w') as hash_file_object:
        ##print >> hash_file_object, checksum_from_file(file_path, hash_method)			## python2.7
        ##print(checksum_from_file(file_path, hash_method), file=hash_file_object)		## python3.5
        hash_file_object.write(checksum_from_file(file_path, hash_method))
