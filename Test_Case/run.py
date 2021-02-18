# -*- coding: utf-8 -*-
# @Time : 2021\1\13 0013 10:27
# @Author : JacksonCui
# @File : run.py
# @Software: PyCharm
import sys,os
sys.path.append(R"C:\Users\Administrator\Desktop\woniuticket")      # 导入代码工程路径
PYTHONPATH = R"C:\Users\Administrator\Desktop\woniuticket\Project" # 导入脚本运行的包路径

import pytest
from Project.Common.DoConfig import DoConf
from Project.Common.Dologs import Logger
from allure_pytest import plugin as allure_plugin
import pytest_repeat as repeat
import pytest_metadata as metadata
# 日志
logger = Logger()



class Run:
    def __init__(self):
        self.conf = DoConf()
        self.allure_results_Path = self.conf.get_value_from_section('project', 'allure_results_Path')
        self.marker = self.conf.get_value_from_section('RunningConfig', 'marker')


    def runWithoutAllure(self):
        logger.info('=' * 10 + f'  RunningTag:{self.marker}  ' + '=' * 10)

        if self.marker.strip() != '':
            args = ['-vs', f'-m {self.marker.lower()}', f'--alluredir={self.allure_results_Path}',
                    f'{os.path.dirname(__file__)}']
            pytest.main(args=args, plugins=[allure_plugin, metadata])
            os.system(f'allure generate {self.allure_results_Path} -o {os.path.dirname(os.path.dirname(__file__))}/Report --clean')

        elif self.marker.strip() != 'ui' or self.marker.strip() != 'api':
            logger.exception('Your running tag must be UI or API')

        else:
            args = ['-vs',  f'--alluredir={self.allure_results_Path}',
                    f'{os.path.dirname(__file__)}']
            pytest.main(args=args, plugins=[allure_plugin, metadata])
            os.system(
                f'allure generate {self.allure_results_Path} -o {os.path.dirname(os.path.dirname(__file__))}/Report --clean')

    # def runWithoutAllure(self):
    #     logger.info('=' * 10 + f'  RunningTag:{self.marker}  ' + '=' * 10)
    #
    #     if self.marker.strip() != '':
    #         args = ['-vs', f'-m {self.marker.lower()}', f'--alluredir={self.allure_results_Path}',
    #                 f'{os.path.dirname(__file__)}']
    #         pytest.main(args=args)
    #         os.system(f'allure generate {self.allure_results_Path} -o {os.path.dirname(os.path.dirname(__file__))}/Report --clean')
    #
    #     elif self.marker.strip() != 'ui' or self.marker.strip() != 'api':
    #         logger.exception('Your running tag must be UI or API')
    #
    #     else:
    #         args = ['-vs',  f'--alluredir={self.allure_results_Path}',
    #                 f'{os.path.dirname(__file__)}']
    #         pytest.main(args=args)
    #         os.system(
    #             f'allure generate {self.allure_results_Path} -o {os.path.dirname(os.path.dirname(__file__))}/Report --clean')
    # def runWithAllure(self):
    #     logger.info('=' * 10 + f'  RunningTag:{self.marker}  ' + '=' * 10)
    #
    #     if self.marker.strip() != '':
    #         args = ['-vs', f'-m {self.marker.lower()}', f'--alluredir={self.allure_results_Path}',
    #                 f'{os.path.dirname(__file__)}']
    #         pytest.main(args=args, plugins=[allure_plugin, repeat])
    #         os.system(
    #             f'allure generate {self.allure_results_Path} -o {os.path.dirname(os.path.dirname(__file__))}/Report --clean')
    #     else:
    #         args = ['-vs', f'--alluredir={self.allure_results_Path}',
    #                 f'{os.path.dirname(__file__)}']
    #         pytest.main(args=args, plugins=[allure_plugin, repeat])
    #         os.system(
    #             f'allure generate {self.allure_results_Path} -o {os.path.dirname(os.path.dirname(__file__))}/Report --clean')
    #     os.system(f'allure serve {self.allure_results_Path}')
if __name__ == '__main__':
    r = Run()
    r.runWithoutAllure()
#     logger.info('='*25+f'  本次运行类型:  '+'='*25)
#
#     pytest.main(['-vs', f'-m UI','--alluredir', f'{os.path.dirname(os.path.dirname(__file__))}/temp',f'{os.path.dirname(__file__)}'])

    # os.system(f'allure generate {os.path.dirname(os.path.dirname(__file__))}/temp -o {reportPath} --clean')
    # os.system(f'allure serve {os.path.dirname(os.path.dirname(__file__))}/temp/')
#     logger.info('=' * 25 + f'  本次运行类型:{marker}  ' + '=' * 25)
#
#     if self.marker.strip() != '':
#         args = ['-vs', f'-m {self.marker.lower()}', f'--alluredir={os.path.dirname(os.path.dirname(__file__))}/temp',
#                 f'{os.path.dirname(__file__)}']
#         pytest.main(args=args, plugins=[allure_plugin, repeat])
#     else:
#         args = ['-vs', f'--alluredir={os.path.dirname(os.path.dirname(__file__))}/temp',
#                 f'{os.path.dirname(__file__)}']
#         pytest.main(args=args, plugins=[allure_plugin, repeat])
#     r = Run()
#     print(r.marker)