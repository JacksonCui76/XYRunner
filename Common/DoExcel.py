# -*- coding: utf-8 -*-
# 版本       ：1.0
# 功能说明    ：PyCharm
# 作者       ：隔壁老王
# 创建时间    ：2021/1/4 14:51
# 修改人      ：无
# 修改日期    ：无

import xlrd
from Project.Common.Dologs import Logger

# 日志
logger = Logger()

class DoExcel():
    '''
    操作（读、写：xlwt、openpyxl）excel文件
    '''
    def __init__(self,filepath):
        self.excle = xlrd.open_workbook(filepath)

    # 返回具体某个sheet对象
    def get_sheet_by_name(self,sheet_name):
        return self.excle.sheet_by_name(sheet_name)

    # 返回当前excel所有的sheet也名称
    def get_all_sheets(self):
        # 以列表的形式返回所有的sheet页
        return self.excle.sheet_names()


