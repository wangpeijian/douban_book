import threading

from db import mysql
from repertory.todo_tags import put_tags, get_todo_list_size, TODO_LIST_WAIT
from util.logger import log


def async_do():
    start = 0
    size = 5

    while True:
        # 待执行任务数超过限制，阻塞当前线程等待唤醒
        todo_size = get_todo_list_size()
        if todo_size > 0:
            log("待执行任务:", todo_size, "，等待唤醒")
            TODO_LIST_WAIT.wait()
            continue

        todo_tags = mysql.find_todo_tags_by_page()
        start = start + size
        log("查询出新的todo_tags:", todo_tags)
        for item in todo_tags:
            tag = item[0]
            page_start = item[1]
            put_tags(tag, page_start)


# 爬取代理的ip地址
def load_task():
    try:
        proxies_thread = threading.Thread(target=async_do)
        proxies_thread.setName("task-loader")
        proxies_thread.start()
    except Exception as e:
        log("待办任务获取异常：", repr(e))
        load_task()
