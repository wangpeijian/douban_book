import threading
import time

from config.system import log_level


def info(*arg):
    if not log_level['info']:
        return

    thread = threading.current_thread()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "   ", thread.getName(), "    :", *arg)


def debug(*arg):
    if not log_level['debug']:
        return

    thread = threading.current_thread()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "   ", thread.getName(), "    :", *arg)
