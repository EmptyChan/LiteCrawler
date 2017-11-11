#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : tasks.py
 @Time       : 2017/10/21 0021 19:27
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description: 申明任务来执行callback, 且必须满足两个参数，一个为requests请求的返回值，一个是自定义的spider请求
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import json
import click
from requests import Response
from lxml import etree
import re
import abc
from log_util import Log
from request import Request
from pipeline import FolderPipeline, ConsolePipeline, FilePipeline
from pipeline import FilePipeline
from utils import TEXT, IMAGE, VIDEO, INDEX, NEXT, DETAIL
qb5200_index_pat = re.compile(r'.*(\d+).*', re.MULTILINE)
qb5200_logger = Log("qb5200")


def qb5200_index_task(response: Response, spider: Request):
    """
    自定义的任务callback函数，这里是index函数
    :param response: requests返回的数据
    :param spider: 自定义的请求
    :return: yeild出新的自定义Request
    """
    html = etree.HTML(response.content.decode('gbk'))
    try:
        all_tr_tags = html.xpath('//div[@id="content"]//tr')
        for tr_tag in all_tr_tags[:2]:  # 请求一本小说，取前两个element,第一个是表格头，第二是小说
            td_temp = tr_tag.xpath('./td[@class="odd"]')
            if len(td_temp):
                name = td_temp[0].xpath('./a/text()')[0]
                url = td_temp[0].xpath('./a/@href')[0]
                yield Request(
                    url, name=name, folder=name, pipeline=FolderPipeline,
                    title=name, callback=qb5200_detail_task, headers={'Referer': spider.url},
                    category=DETAIL
                )
    except Exception as e:
        raise e


def qb5200_detail_task(response: Response, spider: Request):
    """
    自定义的任务callback函数，这里是detail函数
    :param response: requests返回的数据
    :param spider: 自定义的请求
    :return: yeild出新的自定义Request
    """
    html = etree.HTML(response.content.decode('gbk'))
    try:
        base_url = spider.url
        all_td_tags = html.xpath('//table//td')
        for td_tag in all_td_tags:
            a_tag = td_tag.xpath('./a')
            if len(a_tag):
                title = a_tag[0].xpath('./text()')[0]
                folder = title.replace('?', '？')\
                    .replace('!', '！')\
                    .replace('.', '。')\
                    .replace('*', 'x')
                url = a_tag[0].xpath('./@href')
                yield Request(
                    base_url + url[0], name=spider.name, folder=folder, pipeline=FilePipeline,
                    title=title, callback=qb5200_text_task, headers={'Referer': spider.url},
                    category=TEXT
                )
    except Exception as e:
        raise e


def qb5200_text_task(response: Response, spider: Request):
    """
    自定义的任务callback函数，这里是真实数据请求函数，目前为针对于全本小说网的text文本
    :param response: requests返回的数据
    :param spider: 自定义的请求
    :return: yeild出新的自定义Request
    """
    html = etree.HTML(response.content.decode('gbk'))
    try:
        title_temp = html.xpath('//div[@id="title"]')
        if len(title_temp):
            title = title_temp[0].xpath('./text()')[0]
            content_temp = html.xpath('//div[@id="content"]')
            if len(content_temp):
                content = content_temp[0].xpath('string(.)')
                return {
                    "title": str(title),
                    "content": str(content)
                }
    except Exception as e:
        raise e


