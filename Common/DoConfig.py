# -*- coding: utf-8 -*-
# @Time : 2021\1\14 0014 10:42
# @Author : JacksonCui
# @File : DoConfig.py
# @Software: PyCharm
from configparser import ConfigParser
from Project.Common.FilePath import config_path
from Project.Common.Dologs import Logger

# 日志
logger = Logger()


class DoConf:
    def __init__(self):
        self.conf = ConfigParser()
        self.conf.read(config_path, encoding='utf8')

    def get_all_section(self):
        """
        返回所有section的名字
        :return: 列表
        """
        return self.conf.sections()

    def get_all_option_from_section(self, section):
        """
        返回其中一个section下所有option，列表
        :param section:
        :return: list
        """
        return self.conf.options(section)

    def get_value_from_section(self, section, option):
        """
        返回section下其中一个option的值
        :param section: [XXX]
        :param option: option = 值
        :return: str
        """
        return self.conf.get(section, option)

    def get_intValue_from_section(self, section, option):
        """
        返回section下其中一个option的值
        :param section: [XXX]
        :param option: option = 值
        :return: int
        """
        value = None
        try:
            value = int(self.conf.get(section, option))
        except:
            logger.exception('execute task failed. the exception as follows:')

        return value

    def get_all_value_from_option(self, section):
        rlt = []
        for i in self.get_all_option_from_section(section):
            rlt.append(self.get_value_from_section(section, i))
            return rlt

    def get_db_config(self):
        user = self.get_value_from_section('projectDB', 'user')
        pwd = self.get_value_from_section('projectDB', 'pwd')
        port = self.get_intValue_from_section('projectDB', 'port')
        host = self.get_value_from_section('projectDB', 'host')
        db_name = self.get_value_from_section('projectDB', 'db_name')
        li = [host, user, pwd, db_name, port]
        return li
