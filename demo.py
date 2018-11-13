#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#  demo.py
#  python 2.7 / 3.5 - tested
#
#  author: sebastian rollershutter
##
"""testing module file_io - now import/export is json loads/dumps only.
    checksum verification with sha256 checksum by default,
    optional JSONEncoder/decode-method

this demo shows how to import/export own class-instances with conversion-method injection.

add to_dict/from_dict-methods to your class and for importing define a JSONEncoder using to_dict-method from your class.

with builtin types, (nearly) no worries about conversion needed, as they will get converted back to builtin types,
see python docs -> json.
"""
import json
from file_io import import_obj, export_obj


# define a custom class as example, providing conversion to/from dict for json-i/o:
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
class FooEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Foo):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)


####
def main():  # args):
    from os import environ as os_environ

    # setting a file to save/load
    data_path = os_environ['PWD']
    file_name = '%s/demo.json' % data_path

    # setting json.dumps nice-dump-indentation:
    import file_io.import_export_objects_only_json  # .INDENT
    file_io.import_export_objects_only_json.INDENT = None  # 2 # 4

    # testing export/(re-)import with two objects in a loop:
    object_list = [Foo(({"min": 33.33, "avg": 44.44}, 2, 4)),
                   Foo(({"min": 32.23, "avg": 35.53}, 3, 4))]
    for c_obj in object_list:
        export_obj(c_obj, file_name, FooEncoder)  # , 'sha256')

        t_obj = import_obj(file_name, Foo.from_dict)  # , 'sha256')
        print(t_obj, type(t_obj))  # print(out, type(out))

    #### TODO: lists of custom class-instances...
    # test_list = []


####
if __name__ == '__main__':
    import sys
    sys.exit(main())  # sys.argv))
