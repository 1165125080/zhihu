# -*- coding: utf-8 -*-
"""
@Time   : 2018/9/5 21:06
@File   : main.py
@Author : ZZShi
程序作用：

"""
from scrapy import cmdline


cmdline.execute('scrapy crawl zhihu_user'.split())
