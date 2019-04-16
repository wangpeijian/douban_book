import threading

from util.logger import log

# 工作线程阻塞事件
WORKER_WAIT = threading.Event()


def wake_up_worker():
    WORKER_WAIT.set()
    WORKER_WAIT.clear()
    log("唤醒阻塞的工作线程")
