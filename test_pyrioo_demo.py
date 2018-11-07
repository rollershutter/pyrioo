#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_pyrioo.py
#
# TODO: json instead of pickle - done
#
#  author: sebastian rollershutter
####
from os import environ as os_environ
from file_io.import_export_objects \
    import import_obj_with, export_obj_with, \
    read_json, write_json
import time


####
class TestObject():
    def __init__(self, c_id, list_items=[], status=3):
        self.c_id = c_id
        self.created_time = time.time()
        self.status = status
        self.list_items = list_items

    def __str__(self):
        return "{}: id: {}, created: {}, status: {}\n list_items: {}" \
                .format(
                        self.__class__.__name__,
                        self.c_id,
                        self.created_time,
                        self.status,
                        self.list_items)

##
class Test():
    data_path = os_environ['PWD']
    file_name = '%s/testobject.json' % data_path
    test_list = []

    def __init__(self, load_file=False):
        print("# DEBUG Test(): creating new Test instance...")
        if not Test.test_list:
            if load_file:
                self.load_from_file()
            if Test.test_list:
                return
            print("# DEBUG Test: no objects loaded.")

    def _object_from_dict(self, d):
        o = TestObject(d["c_id"])
        if "created_time" in d:
            o.created_time = d["created_time"]
        if "list_items" in d:
            o.list_items = d["list_items"]
        if "status" in d:
            o.status = d["status"]
        return o

    def _objects_from_dicts(self, dict_list):
        _list = []
        for d in dict_list:
            _item = self._object_from_dict(d)
            _list.append(_item)
        return _list

    ##
    def load_from_file(self):
        _list = import_obj_with(Test.file_name, 'sha256', read_json)
        if _list:
            ## convert data for json
            if type(_list[0]) == dict:
                _list = self._objects_from_dicts(_list)
            Test.test_list = _list
        print("\nloaded from file({}):".format(len(Test.test_list)))
        self.print_nice_all(Test.test_list)

    ##
    def save_to_file(self):
        _list = [{'c_id': p.c_id, 'created_time': p.created_time, 'status': p.status, 'list_items': p.list_items} for p in Test.test_list]
        print("saving to file({}):".format(len(Test.test_list)))

        self.print_nice_all(Test.test_list)
        export_obj_with(_list, Test.file_name, 'sha256', write_json)

    ##
    @staticmethod
    def print_nice_all(list_items):
        for o in list_items:
            print(o)


####
def main(args):
    save_file = False
    if len(args) > 1:
        save_file = args[1]

    tt = Test(True)

    if save_file:
        my_list = [TestObject("test-1-2-3"), TestObject("another-4-5-6"), TestObject("dididnanana-7-8-9", {'1': 1234.56, '2': 456.78, '3': 789.12}, 1)]
        Test.test_list = my_list
        tt.save_to_file()

    print("\nbye.")

##
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
