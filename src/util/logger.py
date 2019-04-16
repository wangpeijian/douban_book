import threading


def log(*arg):
    thread = threading.current_thread()
    print(thread.getName(), "    :", *arg)
