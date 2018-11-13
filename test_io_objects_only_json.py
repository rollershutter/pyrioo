#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#  test_io_objects_only_json.py
#  python 2.7 / 3.5 - tested
#
#  author: sebastian rollershutter
##
import json
#import file_io
from file_io import import_obj, export_obj
import file_io.import_export_objects_only_json

# define a custom class as example, providing conversion to dict for json-i/o:
class Foo(object):
    next_id = 0

    def __init__(self, state):
        Foo.next_id += 1
        self.id = Foo.next_id
        self.state = state

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {'class': self.__class__.__name__,
                'id': self.id,
                'state': self.state}

    @staticmethod
    def from_dict(dct):
        if "class" in dct and dct['class'] == Foo.__name__:
            return Foo(dct['state'])
        return dct


# provide a JSONEncoder for custom class Foo using instance-method to_dict():
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Foo):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)


#######################################################################################################################
def main():  # args):
    # testing module file_io.import_export_objects_only_json:
    # now import/export is json.loads/json.dumps only,
    #   with sha256 checksum by default,
    #   with optional JSONEncoder/decode-method
    from os import environ as os_environ

    # setting a file to save/load
    data_path = os_environ['PWD']
    file_name = '%s/test_io_objects.json' % data_path

    # testing export/(re-)import with two objects in a loop:
    object_list = [Foo(({"min": 33.33, "avg": 44.44}, 2, 4)),
                   Foo(({"min": 32.23, "avg": 35.53}, 3, 4)),
                   ]

    file_io.import_export_objects_only_json.INDENT = None  # 2
    for c_obj in object_list:
        #export_obj_with(c_obj.to_dict(), file_name, None, 'sha256')
        export_obj(c_obj, file_name, ComplexEncoder)  # , 'sha256')

        #t_obj = Foo.from_dict(import_obj_with(file_name, None, 'sha256'))
        t_obj = import_obj(file_name, Foo.from_dict)  # , 'sha256')
        print("{}".format(t_obj), type(t_obj))  # print(out, type(out))

    #### TODO: lists of custom class-instances...
    # test_list = []


####
if __name__ == '__main__':
    import sys
    sys.exit(main())  # sys.argv))
