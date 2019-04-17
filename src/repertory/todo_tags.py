import threading

from db import mysql

# 定义全部标签的字典
TAG_TODO_LIST = []

tag_lock = threading.Lock()

# 拉取待办列表的阻塞事件
TODO_LIST_WAIT = threading.Event()


def wake_up_todo_task():
    TODO_LIST_WAIT.set()
    TODO_LIST_WAIT.clear()


def get_todo_list_size():
    return len(TAG_TODO_LIST)


def take_tags():
    tag_lock.acquire()
    wake_up_todo_task()

    tag = None
    page_size = None

    if len(TAG_TODO_LIST) > 0:
        tag_info = TAG_TODO_LIST.pop(0)
        tag = tag_info['tag']
        page_size = tag_info['page_size']

        # 将标签设置为运行中
        mysql.update_tag_doing(tag)

    tag_lock.release()

    return tag, page_size


def put_tags(tag, page_size):
    tag_lock.acquire()
    tag_info = {'tag': tag, 'page_size': page_size}
    TAG_TODO_LIST.append(tag_info)
    tag_lock.release()
