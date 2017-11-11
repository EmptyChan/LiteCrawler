#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : run.py
 @Time       : 2017/11/7 0007 20:40
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description: 运行spider
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from downloader import HttpDownloader
from manager import Manager
from pipeline import ConsolePipeline
from request import Request
from tasks import qb5200_index_task
from utils import INDEX

if __name__ == '__main__':
    '''定义初始的链接请求，初始化到manager中，然后run'''
    req = Request("http://www.qb5200.org/list/3.html", name='qb5200', category=INDEX,
                  pipeline=ConsolePipeline, callback=qb5200_index_task,
                  downloader=HttpDownloader)
    instance = Manager(req)
    instance.run()