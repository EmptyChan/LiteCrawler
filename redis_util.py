#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : redis_util.py
 @Time       : 2017/10/24 0024 21:06
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description: redis相关
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import redis
rdb = redis.Redis(host='localhost', port=6379)
