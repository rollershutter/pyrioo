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

this demo shows how to import/export an iterable containing own class-instances with conversion-method injection.

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


class FooList(object):
    def __init__(self):
        foos = []


    def list_to_dict(self, foo_list): #): #, foo_list):
        return dict((i, foo.to_dict()) for i, foo in enumerate(foo_list)) #self.foos)) #foo_list))

# provide a JSONEncoder for custom class Foo using instance-method to_dict():
class FooListEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FooList) and all(isinstance(f, Foo) for f in obj.foos):
            return obj.list_to_dict(obj.foos) #) #obj.foos)
        return json.JSONEncoder.default(self, obj)



####
def main():  # args):
    from os import environ as os_environ

    # setting a file to save/load
    data_path = os_environ['PWD']
    file_name = '%s/demo_iterable2.json' % data_path

    # setting json.dumps nice-dump-indentation:
    import file_io.import_export_objects_only_json  # .INDENT
    file_io.import_export_objects_only_json.INDENT = 4 #None  # 2 # 4

    ## testing export/(re-)import with two objects in a loop:
    #object_list = [Foo(({"min": 33.33, "avg": 44.44}, 2, 4)),
    #               Foo(({"min": 32.23, "avg": 35.53}, 3, 4))]
    #for c_obj in object_list:
    #    export_obj(c_obj, file_name, FooEncoder)  # , 'sha256')
    #
    #    t_obj = import_obj(file_name, Foo.from_dict)  # , 'sha256')
    #    print(t_obj, type(t_obj))  # print(out, type(out))

    #### TODO: lists of custom class-instances...
    # test_list = []
    # testing export/(re-)import of two objects in an iterable:
    test_list = [Foo(({"min": 33.33, "avg": 44.44}, 2, 2)),
                   Foo(({"min": 32.23, "avg": 35.53}, 3, 4)),
                   Foo(({"min": 36.63, "avg": 38.83}, 4, 3))]
    foo_list = FooList()
    foo_list.foos = test_list
    print("exporting %s" % foo_list.foos)
    export_obj(foo_list, file_name, FooListEncoder)



####
if __name__ == '__main__':
    import sys
    sys.exit(main())  # sys.argv))
