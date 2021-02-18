# -*- coding: utf-8 -*-
# @Time : 2021\2\17 0017 22:01
# @Author : JacksonCui
# @File : Tool.py
# @Software: PyCharm
class QSSTool:
    @classmethod
    def qss2obj(cls,filePath,obj):
        with open(filePath,'r') as f:
            content = f.read()
            obj.setStyleSheet(content)