from lxml import etree

from db import mysql
from impl import book_scan
from impl import http
from impl import task_loader
from repertory.todo_tags import put_tags
from util.logger import info


# 爬取热门标签列表
def get_init_tags():
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'

    data = http.req_url(url)
    s = etree.HTML(data)

    tag_list = s.xpath('//*[@class="tagCol"]/tbody/tr/td/a/text()')

    info(tag_list)

    # 从正常入口扫描
    for tag in tag_list:
        put_tags(tag, 0)
        # 新增一个tag
        mysql.add_tag(tag)


# 输出项目当前进度
def print_task_progress():
    # 恢复中断的tag状态
    mysql.tags_reset()

    done_tags = mysql.find_todo_tags(1)
    todo_tags = mysql.find_todo_tags(0)

    done_size = len(done_tags)
    todo_size = len(todo_tags)

    info('======================================================')
    info('已经完成的tag:', done_size)
    info('======================================================')

    info('======================================================')
    info('待执行的tag:', todo_size)
    info('======================================================')
    return done_size, todo_size


# 增量入口
def increment_entry():
    done_size, todo_size = print_task_progress()

    # 没有数据时走正常拉取，从热门列表开始爬取
    if done_size == 0 and todo_size == 0:
        get_init_tags()

    # 开启线程加载待办任务
    task_loader.load_task()

    # 扫描待办任务
    book_scan.scan()


# 测试入口
def test_entry():
    put_tags("科幻", 456)
    book_scan.scan()
