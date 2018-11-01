#!/usr/local/bin/python
#-*- encoding: UTF-8 -*-

import logging


class blog:
    def __init__(self,type,log_name,log_level):
            self.log_name   = log_name
            self.log_level  = log_level
            self.type       = type

    def getLog(self):
            str_format = '%(asctime)s %(levelname)s > %(message)s'
            logging.basicConfig(
                            level   = self.log_level,
                            format  = str_format,
                            datefmt = '%Y-%m-%d %X',
                            filename        = self.log_name,
                            filemode        = 'a')
            if self.type != "d":
                    return logging.getLogger(self.log_name)

            #mlog = logging.getLogger(self.log_name)
            console = logging.StreamHandler()
            console.setLevel(self.log_level)
            formatter = logging.Formatter(str_format)
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
            mlog = logging.getLogger(self.log_name)
            mlog.info("logging test .....!by davidsun")

            return mlog


if __name__ == '__main__':
    log = blog("d", "test_log.log", 10).getLog()
    log.info("hahaha!")