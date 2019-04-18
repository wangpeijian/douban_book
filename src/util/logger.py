import threading
import time

from config.system import log_level


def error(*arg):
    if not log_level['error']:
        return

    thread = threading.current_thread()
    print('\033[31m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " 【ERROR】 ", thread.getName(), "  :", *arg)


def info(*arg):
    if not log_level['info']:
        return

    thread = threading.current_thread()
    print('\033[0m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " 【INFO】 ", thread.getName(), "  :", *arg)


def debug(*arg):
    if not log_level['debug']:
        return

    thread = threading.current_thread()
    print('\033[0m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " 【DEBUG】 ", thread.getName(), "  :", *arg)
