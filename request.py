#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : request.py
 @Time       : 2017/10/21 0021 17:25
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description: 自定义Reuqest类
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import json
import click
from hashlib import md5
import time
import datetime
from utils import ua
from downloader import HttpDownloader


class Request(object):
    """
    请求类
    """
    def __init__(self, url, name, title=None,
                 folder=None, headers=None, callback=None, pipeline=None,
                 downloader=None,
                 category=None, proxy=None):
        """
        初始化
        :param url: 请求链接
        :param name: 请求名称，用来作为存放的文件夹名称以及mongo的集合名
        :param title: 存放到mongo的信息
        :param folder: 存放image或者video的子文件夹名称或者存放text的文件名
        :param headers: 请求头
        :param callback: 回调函数
        :param pipeline: 处理管道
        :param downloader: 下载器
        :param category: 类别，定义在工具类中，作为mongo的集合名
        :param proxy: 代理
        """
        super(object, self).__init__()
        self.name = name
        self.category = category
        self.url = url
        headers_temp = {"User-Agent": ua.random}
        if headers:
            headers_temp.update(headers)
        r = md5()
        __id = '{url}+{headers}'.format(url=url, headers=headers_temp)
        r.update(__id.encode('utf-8'))
        self.id = r.hexdigest()
        self.title = title
        self.folder = folder
        self.headers = headers_temp
        self.pipeline = pipeline
        if not downloader:
            downloader = HttpDownloader
        self.downloader = downloader
        self.callback = callback
        self.proxy = proxy

    def __call__(self, *args, **kwargs):
        """
        存放到mongo
        :param args: 位置参数
        :param kwargs: 命名参数
        :return:
        """
        return {"_id": self.id,
                "name": self.name,
                "url": self.url,
                "title": self.title,
                "folder": self.folder,
                "category": self.category,
                "date": datetime.datetime.utcnow(),
                "timestamp": time.time() * 1000}

    def to_dict(self):
        """
        序列化
        :return:
        """
        return {"name": self.name,
                "url": self.url,
                "title": self.title,
                "headers": self.headers,
                "folder": self.folder,
                "pipeline": self.pipeline,
                "category": self.category,
                "downloader": self.downloader,
                "callback": self.callback,
                "proxy": self.proxy}

    @staticmethod
    def from_dict(di):
        """
        反序列化
        :param di: 从redis取出的序列化的数据
        :return:
        """
        cb = di['callback']
        # import dictionary
        # callback = dictionary.TASK[cb]
        name = di['name']
        title = di['title'] if di['title'] else None
        headers = di['headers'] if di['headers'] else None
        folder = di['folder'] if di['folder'] else None
        proxy = di['proxy'] if di['proxy'] else None
        return Request(url=di['url'],
                       name=name,
                       title=title,
                       headers=headers,
                       folder=folder,
                       pipeline=di['pipeline'],
                       category=di['category'],
                       downloader=di['downloader'],
                       callback=cb,
                       proxy=proxy)
