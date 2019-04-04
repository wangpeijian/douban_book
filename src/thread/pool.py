import threading

from thread import load_thread


class ThreadPool:

    def __init__(self, size):
        self.size = size
        self.event = threading.Event()
        self.threadLock = threading.Lock()
        self.threadReleaseLock = threading.Lock()

        self.running_thread = []
        self.free_thread = []

        i = 1
        while i <= size:
            self.free_thread.append(i)
            i = i + 1

    def fetch_id(self):
        self.threadReleaseLock.acquire()
        thread_id = self.free_thread.pop()
        self.running_thread.append(thread_id)
        self.threadReleaseLock.release()
        return thread_id

    # 线程结束释放一个id
    def release_id(self, thread_id):
        self.threadReleaseLock.acquire()
        self.free_thread.append(thread_id)
        self.running_thread.remove(thread_id)
        self.event.set()
        self.threadReleaseLock.release()

    def submit(self, tag, page_start):

        self.threadLock.acquire()

        while len(self.free_thread) == 0:
            self.event.wait()
        else:
            # 从free_thread中获取一个空闲的线程号
            thread = load_thread.LoadThread(tag, page_start, self)
            thread.start()

        self.threadLock.release()


# def main():
#     thread_pool = ThreadPool(5)
#     lop = 0
#     while lop < 10:
#         thread_pool.submit("测试：%s" % lop, 0)
#         lop = lop + 1
