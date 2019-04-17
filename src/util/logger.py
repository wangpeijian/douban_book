import threading
import time


def log(*arg):
    thread = threading.current_thread()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "   ", thread.getName(), "    :", *arg)
