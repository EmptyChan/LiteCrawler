#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : log_util.py
 @Time       : 2017/10/29 0029 13:24
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description: log相关类
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import logging
import time
import logging.handlers

import os

rq = time.strftime('%Y%m%d', time.localtime(time.time()))


class Log(object):
    """
    日志类
    """
    def __init__(self, name):
        self.path = "./log/"  # 定义日志存放路径
        if not os.path.exists('{0}{1}'.format(self.path, name)):
            os.mkdir('{0}{1}'.format(self.path, name))
        self.filename = "{0}{1}/{2}.log".format(self.path, name, rq)     # 日志文件名称
        self.name = name    # 为%(name)s赋值
        self.logger = logging.getLogger(self.name)
        # 第一步，创建一个logger
        self.logger.setLevel(logging.INFO)  # Log等级总开关

        # 第二步，创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.filename, mode='w')
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

        # 第三步，再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

        # 第四步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 第五步，将logger添加到handler里面
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)



