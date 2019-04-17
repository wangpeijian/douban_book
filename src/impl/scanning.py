from lxml import etree

from core import const
from core import execute
from db import mysql
from impl import http
from util.logger import log

# 定义全部标签的字典
tag_dict = {}

# 当前正在执行的标签列表
tag_dict_current = {}


# 根据扩展扫描到的tag递归爬取数据
def scan_todo_list():
    todo_tags = tag_dict_current.keys()
    if len(todo_tags) != 0:
        for tag in todo_tags:
            # 多线程实现
            # ========================================
            # 使用多线程爬取数据
            page_size = tag_dict_current.get(tag, 0)
            const.THREAD_EXECUTE.submit(execute.Execute(tag, page_size))
            # ========================================


# 爬取热门标签列表
def get_init_tags():
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'

    data = http.req_url(url)
    s = etree.HTML(data)

    tag_list = s.xpath('//*[@class="tagCol"]/tbody/tr/td/a/text()')

    log(tag_list)

    # 从正常入口扫描
    for tag in tag_list:
        tag_dict_current[tag] = 0
        # 新增一个tag
        mysql.add_tag(tag)


# 增量入口
def increment_entry():
    done_tags = mysql.find_todo_tags(1)
    for item in done_tags:
        tag = item[0]
        page_start = item[1]
        log('已经完成的tag:', tag, page_start)
        tag_dict[tag] = page_start
    log('======================================================')

    todo_tags = mysql.find_todo_tags(0)
    for item in todo_tags:
        tag = item[0]
        page_start = item[1]
        log('待执行的tag:', tag, page_start)
        tag_dict_current[tag] = page_start
    log('======================================================')

    # 没有数据时走正常拉取，从热门列表开始爬取
    if len(done_tags) == 0 and len(todo_tags) == 0:
        get_init_tags()

    scan_todo_list()


def test_entry():
    tag_dict_current['科幻'] = 434
    scan_todo_list()
