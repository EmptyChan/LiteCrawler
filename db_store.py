#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : db_store.py
 @Time       : 2017/10/24 0024 19:14
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description: database相关的内容
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import click
from pymongo import MongoClient

# 建立MongoDB数据库连接
client = MongoClient('localhost', 27017)
db = client.images_db


def mongo_map(name):
    """
    mongo db的映射
    :param name: 创建的mongo集合名称
    :return: mongo集合，类似于表格
    """
    return eval('db.{0}'.format(name))


if __name__ == '__main__':
    mongo_map('cjh').insert_one({'ssss': 123})