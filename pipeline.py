#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : pipeline.py
 @Time       : 2017/10/21 0021 16:31
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description: 文件处理管道
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import json
import click
import os
from requests import Response
from utils import TEXT, IMAGE, VIDEO
from request import Request
import abc


class BasePipeline(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def store(self, data: Response, spider: Request) -> bool:
        pass

    @abc.abstractmethod
    def exist(self, spider: Request) -> bool:
        pass


class FilePipeline(BasePipeline):
    """
    文件处理管道
    """
    def __init__(self):
        super().__init__()

    def store(self, data: Response, spider: Request) -> bool:
        """
        储存文件
        :param data: requests返回的数据
        :param spider: 请求的自定义request
        :return: 存储是否成功
        """
        if not data:
            click.echo('data is None')
            return False
        main_folder = str(spider.name).lower()
        if not os.path.exists('../{0}/{1}'.format(spider.category, main_folder)):
            os.mkdir('../{0}/{1}'.format(spider.category, main_folder))
        if spider.category == IMAGE:
            query = '../{0}/{1}/{2}/{3}.jpg'.format(spider.category, main_folder, spider.folder, spider.id)
            with open(query, mode='wb') as f:
                f.write(data.content)
                click.echo("save %s in %s" % (spider.category, query))
                click.echo("save %s===>>>%s" % (spider.category, spider.url))
        elif spider.category == TEXT:
            query = '../{0}/{1}/{2}.txt'.format(spider.category, main_folder, spider.folder)
            if spider.callback:
                result = spider.callback(data, spider)
                with open(query, mode='w', encoding='utf-8') as f:
                    f.writelines(result.get('title'))
                    f.writelines(result.get('content'))
                    click.echo("save %s in %s" % (spider.category, query))
                    click.echo("save %s===>>>%s" % (spider.category, spider.url))
        return True

    def exist(self, spider: Request) -> bool:
        """
        判断文件是否存在
        :param spider: 请求的自定义request
        :return: 文件是否存在
        """
        main_folder = str(spider.name).lower()
        query = None
        if spider.category == IMAGE:
            query = '../{0}/{1}/{2}/{3}.jpg'.format(spider.category, main_folder, spider.folder, spider.id)
        elif spider.category == TEXT:
            query = '../{0}/{1}/{2}.txt'.format(spider.category, main_folder, spider.folder)
        if not query:
            return False
        if os.path.exists(query):
            return True
        return False


class FolderPipeline(BasePipeline):
    """
    文件夹处理
    """
    def __init__(self):
        super().__init__()

    def store(self, data: Response, spider: Request) -> bool:
        """
        文件夹处理
        :param data: requests返回的数据
        :param spider: 请求的自定义request
        :return: 文件夹创建是否成功
        """
        click.echo("***************")
        click.echo(spider.id)
        click.echo(spider.name)
        click.echo(spider.url)
        main_folder = str(spider.name).lower()
        query = '.'
        if spider.category == TEXT or spider.category == IMAGE:
            query = '../{0}/{1}'.format(spider.category, main_folder)
        if not os.path.exists(query):
            os.mkdir(query)
        if spider.category == IMAGE:
            if not os.path.exists('%s/%s' % (query, spider.folder)):
                os.mkdir('%s/%s' % (query, spider.folder))
                click.echo(' create folder=>>> %s/%s' % (query, spider.folder))
            click.echo("@@@@@@@@@@@@@@@")
        return True

    def exist(self, spider: Request) -> bool:
        return False


class ConsolePipeline(BasePipeline):
    """
    控制台输出
    """
    def __init__(self):
        super().__init__()

    def store(self, data: Response, spider: Request) -> bool:
        click.echo("***************")
        click.echo(spider.id)
        click.echo(spider.name)
        click.echo(spider.url)
        click.echo("@@@@@@@@@@@@@@@")
        return True

    def exist(self, spider: Request) -> bool:
        return False
