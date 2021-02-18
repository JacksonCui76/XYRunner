# -*- coding: utf-8 -*-
# @Time : 2021\1\14 0014 16:29
# @Author : JacksonCui
# @File : DoAssert.py
# @Software: PyCharm
"""通用断言"""
from Project.Common.Dologs import Logger

# 日志
logger = Logger()

class DoAssert:
    @classmethod
    def should_contain(cls, exp, rlt):
        if rlt:
            logger.info(f'exp>>{exp}')
            logger.info(f'rlt>>{rlt}')
            assert exp in rlt

    @classmethod
    def should_equal(cls, exp, rlt):
        logger.info(f'exp>>{exp}')
        logger.info(f'rlt>>{rlt}')
        assert exp == rlt

    @classmethod
    def len_should_greater(cls, exp, rlt):
        logger.info(f'exp>>{exp}')
        logger.info(f'rlt>>{rlt}')
        exp = int(exp)
        rlt = len(rlt)
        assert exp < rlt

    @classmethod
    def should_none(cls, exp, rlt):

        exp = eval(exp)
        logger.info(f'exp>>{exp}')
        logger.info(f'rlt>>{rlt}')
        assert exp is rlt

    @classmethod
    def doAssert(cls, exp, rlt, AssertType):
        if AssertType in ('response', 'rp'):
            cls.should_contain(exp, rlt)
        elif AssertType in ('length', 'len'):
            cls.len_should_greater(exp, rlt)
        elif AssertType in ('None',):
            cls.should_none(exp, rlt)
