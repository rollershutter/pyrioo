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
# from file_io.import_export_objects import IO_DEBUG as io_debug
import file_io
import time


####
class TestObject():
    def __init__(self, c_id, dict_items={}, status=3):
        self.c_id = c_id
        self.created_time = time.time()
        self.status = status
        self.dict_items = dict_items

    @staticmethod
    def _obj_to_dict(obj):
        """
        creates dict from a given TestObject-object.
        :return TestObject instance
        """
        return {'c_id': obj.c_id,
                'created_time': obj.created_time,
                'status': obj.status,
                'dict_items': obj.dict_items}

    def to_dict(self):
        return self._obj_to_dict(self)

    #def __cmp__(self):
    #    pass

    def __eq__(self, other):
        """
        :type other: TestObject
        """
        if not isinstance(other, self.__class__):
            raise ValueError("cannot compare object: not of type TestObject.")  # return False
        return self.to_dict() == other.to_dict()  # all([self.c_id, self.created_time, ])

    def __str__(self):
        return "{}: id: {}, created: {}, status: {}\n dict_items: {}" \
                .format(
                        self.__class__.__name__,
                        self.c_id,
                        self.created_time,
                        self.status,
                        self.dict_items)

##
class Test():
    data_path = os_environ['PWD']
    file_name = '%s/testobject.json' % data_path
    test_list = []

    def __init__(self, load_file=False):
        print("# DEBUG Test: creating new Test instance...")
        if not Test.test_list:
            if load_file:
                self.load_from_file()
            if Test.test_list:
                return
            print("# DEBUG Test: no objects loaded.")

    @staticmethod
    def _dict_from_object(obj):
        """
        creates dict from a given TestObject-object.
        :return TestObject instance
        """
        #return {'c_id': obj.c_id,
        #        'created_time': obj.created_time,
        #        'status': obj.status,
        #        'dict_items': obj.dict_items}
        return obj.to_dict()

    @staticmethod
    def _object_from_dict(d):
        """
        creates TestObject-object from a given, suitable dict.
        :return TestObject instance
        """
        obj = TestObject(d["c_id"])
        if "created_time" in d:
            obj.created_time = d["created_time"]
        if "dict_items" in d:
            obj.dict_items = d["dict_items"]
        if "status" in d:
            obj.status = d["status"]
        return obj

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
        #_list = [{'c_id': p.c_id, 'created_time': p.created_time, 'status': p.status, 'dict_items': p.dict_items} for p in Test.test_list]
        _list = [p.to_dict() for p in Test.test_list]
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
    #file_io.import_export_objects.IO_DEBUG = False
    file_io.import_export_objects.IO_DEBUG = True  # False

    for save_file, load_file in ((False, True), (True, False)):
        #save_file = False  # True  # False
        if len(args) > 1:
            save_file = args[1]

        print("#"*24, "testing import/export python objects:", sep="\n")
        tt = Test(load_file)  # True)  # False)  # (True)

        if save_file:
            my_list = [TestObject("test-1-2-3"), TestObject("another-4-5-6", {'1': 912.34, '2': 345.67}, 2), TestObject("dididnanana-7-8-9", {'1': 1234.56, '2': 456.78, '3': 789.12}, 1)]
            Test.test_list = my_list
            tt.save_to_file()

        tt_old = Test.test_list[::]
        tt.load_from_file()

        for l in (tt_old, Test.test_list, tt.test_list):
            print(l.__class__.__name__, hex(id(l)), len(l))

        try:
            #assert(all((tt.test_list == tt_old, Test.test_list == tt_old, Test.test_list == tt.test_list)))
            assert(tt.test_list == tt_old == Test.test_list)
            #print(list(zip([1, 2, 3], [4, 5, 6])))
            #print([a == b for a, b in list(zip(tt_old, tt.test_list))])
            assert(all(a == b for a, b in list(zip(tt_old, tt.test_list))))
            #assert(all(tt.test_list == tt_old))
            print("tests passed.\n")
        except:
            print("tests failed!\n")

    print("\nbye.")

##
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
