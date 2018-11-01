# coding=utf-8

import os
import MySQLdb

class filectl():
    _filename = ""

    def __init__(self, filename = ""):
        super(filectl, self).__init__()


        self._filename = filename
        self._cur_idx = 0
        print os.getcwd()
        self.load_ctl_file()

    def write_file(self, filename, content):
        """文件持久化"""

    def load_ctl_file(self):
        if not os.path.exists("control"):
            os.makedirs("control")
        print "#####" + os.getcwd()
        file_name = "control/setup_idx_control.txt"
        fd = open(file_name, 'rw+')
        # fd.write(str(self._max_idx))

        # idx_str = fd.readline().strip()
        line = fd.readline()
        print "88888:" + line

        if line.__len__() > 0:
            self._max_idx = int(line)
            print "read max idx " + str(self._max_idx)
        else:
            self._max_idx = 0
            print str(self._max_idx)
            fd.write(str(self._max_idx))

    def load_ctl_file(self, num = 0):
        file_name = "control/setup_idx_control.txt"
        fd = open(file_name, 'rw+')

        if str(num).__len__() > 0:
            self._max_idx = int(line)
            print "updata idx :" + str(self._max_idx)
            fd.write(str(num))

        fd.close()
