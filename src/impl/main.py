#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading

import requests
from lxml import etree

from impl import mysql
from thread import pool

# 线程同步锁
threadLock = threading.Lock()

# 定义全部标签的字典
tag_dict = {}

# 当前正在执行的标签列表
tag_dict_current = {}

# 线程池大小
THREAD_POOL = pool.ThreadPool(10)


# 请求方法
def req_url(url):
    return requests.get(url).text


# 记录代办的标签列表
def record_todo_tags(tags):
    for tag in tags:
        if tag_dict.get(tag) is None and tag_dict_current.get(tag) is None:
            tag_dict_current[tag] = 0
            # 新增一个tag
            mysql.add_tag(tag)


# 根据标签加载某一标签下的全部图书数据
def load_tag(tag, page_start):
    url = 'https://book.douban.com/tag/' + tag + '?start=' + str(page_start) + '&type=T'
    print(url)

    data = req_url(url)
    s = etree.HTML(data)

    # 扫描相关的标签并记录
    ref_tags = s.xpath('//*[@class="tags-list"]/a/text()')
    record_todo_tags(ref_tags)

    url_list = s.xpath('//*[@class="subject-item"]/div/h2/a/@href')

    print("====扫描到的列表数据", url_list)

    index = 0
    for url in url_list:
        #  根据图书详情页面链接爬取 评分，常用标签，简介， 图书名称
        detail_data = req_url(url)
        detail_tree = etree.HTML(detail_data)

        tags = detail_tree.xpath('//*[@class="indent"]/span/a/text()')
        rating = detail_tree.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')
        title = detail_tree.xpath('//*[@id="wrapper"]/h1/span/text()')
        intro = detail_tree.xpath('//*[@class="intro"]/p/text()')

        # 记录相关标签
        record_todo_tags(tags)

        res = url.split("/")

        _id = res[4]
        _book_name = title[0].strip()
        _tags = "|".join(tags)
        _intro = "".join(intro)
        _rating = rating[0].strip()
        _url = url

        print(
            '图书链接：', url,
            '图书id：', _id,
            '图书名称：', _book_name,
            '图书评分：', _rating,
            '图书标签：', _tags,
            '图书简介：', _intro
        )

        # 保存图书信息
        mysql.add_book(_id, _book_name, _tags, _intro, _rating, _url)

        index = index + 1

    # 循环结束更新当前查询进度
    mysql.update_tag_start(tag, page_start + len(url_list))

    if len(url_list) != 0:
        load_tag(tag, page_start + 20)
    else:
        return


# 根据扩展扫描到的tag递归爬取数据
def scan_todo_list():
    # 扫描过程中收集到的标签列表继续无限循环
    todo_map = tag_dict_current.copy()
    todo_tags = todo_map.keys()
    if len(todo_tags) != 0:
        for tag in todo_tags:
            # 单线程实现
            # ========================================
            # 爬取新标签数据，如果存在记录的条数，则继续查询
            # load_tag(tag, todo_map.get(tag, 0))
            # 更新tag状态,tag标记为完成状态
            # mysql.update_tag_done(self.tag)
            # ========================================

            # 多线程实现
            # ========================================
            # 使用多线程爬取数据
            THREAD_POOL.submit(tag, todo_map.get(tag, 0))
            # ========================================

            tag_dict[tag] = 1
            tag_dict_current.pop(tag)

        # 递归查询
        scan_todo_list()
    else:
        return


# 爬取热门标签列表
def normal_entry():
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'

    data = requests.get(url).text
    s = etree.HTML(data)

    tag_list = s.xpath('//*[@class="tagCol"]/tbody/tr/td/a/text()')

    print(tag_list)

    # 从正常入口扫描
    for tag in tag_list:
        tag_dict_current[tag] = 0
        # 新增一个tag
        mysql.add_tag(tag)

    scan_todo_list()


# 增量入口
def increment_entry():
    done_tags = mysql.fond_todo_tags(1)
    for item in done_tags:
        tag = item[0]
        page_start = item[1]
        print('已经完成的tag:', tag)
        tag_dict[tag] = page_start
    print('======================================================')

    todo_tags = mysql.fond_todo_tags(0)
    for item in todo_tags:
        tag = item[0]
        page_start = item[1]
        print('待执行的tag:', tag)
        tag_dict_current[tag] = page_start
    print('======================================================')

    # 没有数据时走正常拉取，从热门列表开始爬取
    if len(done_tags) == 0 and len(todo_tags) == 0:
        normal_entry()
    else:
        scan_todo_list()
