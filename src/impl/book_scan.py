import threading
import time

from core import const
from core import execute
from repertory.todo_tags import take_tags
from util.logger import log


def async_do():
    while True:
        tag, page_size = take_tags()
        if tag is not None:
            print("准备执行的任务:", tag, page_size)
            const.THREAD_EXECUTE.submit(execute.Execute(tag, page_size))
        else:
            time.sleep(1)


# 爬取代理的ip地址
def scan():
    try:
        proxies_thread = threading.Thread(target=async_do)
        proxies_thread.setName("task-loader")
        proxies_thread.start()
    except Exception as e:
        log("提交任务异常：", repr(e))
        scan()
