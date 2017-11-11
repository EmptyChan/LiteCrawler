#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : manager.py
 @Time       : 2017/11/5 0005 11:33
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description: 主要的管理类
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import json

import click
import time
from request import Request
import grequests
from log_util import Log
from redis_util import rdb
from retrying import retry
from db_store import mongo_map
from utils import TEXT, INDEX, IMAGE, VIDEO, NEXT, DETAIL
import pickle as cPickle
import time


def exception_handler(requests, exception):
    """
    grequests的错误异常处理
    :param requests: 请求链接
    :param exception: 异常信息
    :return: None
    """
    click.echo(exception)


class Manager(object):
    """
    管理器
    """
    def __init__(self, start_request: Request):
        """
        初始化
        :param start_request: 初始化的自定义request
        """
        super().__init__()
        self.rdb = rdb
        self.start_request = start_request
        self.append_spider(start_request)
        self.task_list = []  # 辅助并发请求
        self.logger = Log(name='Manager')
        self.req_count = 0
        self.count = 0

    def append_spider(self, req):
        """
        添加到redis
        :param req: 自定义request
        :return: None
        """
        temp = cPickle.dumps(req.to_dict(), protocol=-1)
        self.rdb.rpush(self.start_request.id, temp)

    @retry(stop_max_attempt_number=3, wait_random_min=0, wait_random_max=200)
    def __request(self, spiders: list):
        """
        并发批量请求，用于image和video
        :param spiders: 自定义request集合
        :return: 请求的数据集合
        """
        url_list = []
        self.logger.info('start batch request!')
        for url in spiders:
            if url.proxy:
                url_list.append(grequests.get(url.url, headers=url.headers, proxies=url.proxy, timeout=10))
            else:
                url_list.append(grequests.get(url.url, headers=url.headers, timeout=10))
        self.logger.info('all complete!')
        return grequests.map(url_list, exception_handler=exception_handler)

    def handle(self, spider: Request):
        """
        redis中取出的request处理
        :param spider: 自定义的request
        :return: None
        """
        gallery = mongo_map(spider.name)
        self.req_count += 1
        if self.req_count == 50:
            time.sleep(3)
            self.req_count = 0
        if spider.category == IMAGE \
                or spider.category == VIDEO:
            retry_list = []
            if not gallery.find_one({"_id": spider.id}):
                gallery.insert_one(spider())
            if not spider.pipeline.exist(spider.pipeline, spider):
                self.task_list.append(spider)
            if 20 >= len(self.task_list) >= 10 or self.count < 10:  # 并发处理
                res_list = self.__request(self.task_list)
                for i, res in enumerate(res_list):
                    if not self.task_list[i].pipeline.store(self.task_list[i].pipeline, data=res, spider=self.task_list[i]):
                        retry_list.append(spider)
                self.task_list.clear()
                self.task_list.extend(retry_list)
                retry_list.clear()
        elif spider.category == INDEX \
                or spider.category == NEXT \
                or spider.category == DETAIL:
            # start = time.time()
            res = spider.downloader.request(spider.downloader, spider=spider)
            # end = time.time()
            # click.echo('request consume %s' % str(end - start))
            spider.pipeline.store(spider.pipeline, data=res, spider=spider)
            # start = time.time()
            # click.echo('store consume %s' % str(start - end))
            if spider.callback:
                result = spider.callback(res, spider)
                for sp in result:
                    if not gallery.find_one({"_id": sp.id}):
                        gallery.insert_one(sp())
                    self.append_spider(sp)
        elif spider.category == TEXT:
            res = spider.downloader.request(spider.downloader, spider=spider)
            spider.pipeline.store(spider.pipeline, data=res, spider=spider)

    def run(self):
        """
        运行
        :return: None
        """
        self.count = self.rdb.llen(self.start_request.id)
        while self.count:
            spider = None
            try:
                click.echo('start spider.....')
                start = time.time()
                temp = self.rdb.lpop(self.start_request.id)
                by = cPickle.loads(temp)
                spider = Request.from_dict(by)
                end = time.time()
                click.echo('get spider consume %s' % str(end - start))
                self.handle(spider)
                click.echo('handle complete!')
            except Exception as e:
                # time.sleep(0.1)
                # if spider:
                #     self.append_spider(spider)
                raise e
            self.count = self.rdb.llen(self.start_request.id)
