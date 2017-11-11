#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : downloader.py
 @Time       : 2017/10/21 0021 16:31
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description: 下载器
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from retrying import retry
import requests
import grequests
import json
import click


class HttpDownloader(object):
    """
    http下载器
    """
    def __init__(self):
        super().__init__()

    @retry(stop_max_attempt_number=3, wait_random_min=0, wait_random_max=200)
    def request(self, spider):
        """
        自定义请求
        :param spider: 自定义请求的request，可以是list
        :return: 返回请求数据
        """
        if isinstance(spider, list):
            url_list = []
            for url in spider:
                url_list.append(grequests.get(url.url, headers=url.headers))
            return grequests.map(url_list)
        else:
            if spider.proxy:
                return requests.get(spider.url, headers=spider.headers, proxies=spider.proxy, timeout=60)
            else:
                return requests.get(spider.url, headers=spider.headers, timeout=60)