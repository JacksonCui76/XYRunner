# -*- coding: utf-8 -*-
# @Time : 2021\1\14 0014 10:44
# @Author : JacksonCui
# @File : FilePath.py
# @Software: PyCharm
import os

# 配置中心文件
config_path = os.path.dirname(os.path.dirname(__file__)) + r'/Config/config.ini'
# 用例excel表
CaseFile_path = os.path.dirname(os.path.dirname(__file__)) + r'/CaseFile/casefile.xlsx'
# 截图文件夹
img_path = os.path.dirname(os.path.dirname(__file__)) + r'/screenshot'
# 日志文件
logger_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/logs/Catalina.out'
# run.py 主入口
run_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/Test_case/run.py'
# html 文件
html_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/Report/index.html'
