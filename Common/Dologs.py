# -*- coding: utf-8 -*-
# @Time : 2021\2\5 0005 13:56
# @Author : JacksonCui
# @File : Dologs.py
# @Software: PyCharm

import logging, os
import logging.config
from Project.Common.FilePath import logger_path


class Logger(object):
    """
    封装好的Logger工具
    """

    def __init__(self, logPath=logger_path):
        """
        initial
        """
        log_path = logPath
        logging.addLevelName(20, "INFO:")
        logging.addLevelName(30, "WARNING:")
        logging.addLevelName(40, "ERROR:")
        logging.addLevelName(50, "ERROR:")
        logging.basicConfig(level=logging.DEBUG,
                            format="%(levelname)s %(asctime)s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            filename=log_path,
                            filemode="a"
                            )
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s  %(message)s")
        console.setFormatter(formatter)
        logging.getLogger("").addHandler(console)

    def debug(self, msg=""):
        """
        output DEBUG level LOG
        """
        logging.debug(str(msg))

    def info(self, msg=""):
        """
        output INFO level LOG
        """
        logging.info(str(msg))

    def warning(self, msg=""):
        """
        output WARN level LOG
        """
        logging.warning(str(msg))

    def exception(self, msg=""):
        """
        output Exception stack LOG
        """
        logging.exception(str(msg))

    def error(self, msg=""):
        """
        output ERROR level LOG
        """
        logging.error(str(msg))

    def critical(self, msg=""):
        """
        output FATAL level LOG
        """
        logging.critical(str(msg))


if __name__ == "__main__":
    testlog = Logger()
    try:
        lists = []
        print(lists[1])
    except :
        # raise Exception('123')
        testlog.exception("execute task failed. the exception as follows:")
        exit(1)
