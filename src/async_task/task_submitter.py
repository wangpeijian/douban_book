import threading
import time

from core import const
from core import execute
from repertory.todo_tags import take_tags
from util.logger import info, error


def async_do():
    while True:
        tag, page_size = take_tags()
        if tag is not None:
            info("准备执行的任务:", tag, page_size)
            const.THREAD_EXECUTE.submit(execute.Execute(tag, page_size))
        else:
            time.sleep(1)


# 爬取代理的ip地址
def start():
    try:
        proxies_thread = threading.Thread(target=async_do)
        proxies_thread.setName("task-submitter")
        proxies_thread.start()
    except Exception as e:
        error("提交任务异常：", repr(e))
        start()
