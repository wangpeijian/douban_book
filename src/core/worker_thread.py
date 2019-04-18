import threading
import time

from util.logger import error

# 缓存线程池缓存时间
CACHE_TIME = 60
# 单次睡眠时间
SLEEP_TIME = 0.1


class Worker(threading.Thread):
    def __init__(self, thread_id, thread_pool):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = "book-loader-%s" % thread_id
        self.thread_pool = thread_pool

    # 线程运行
    def run(self):

        loop = 0
        while SLEEP_TIME * loop < CACHE_TIME:
            # 从线程池任务队列中获取任务，没有任务则休眠，超过休眠时间则释放线程
            execute_task = self.thread_pool.take_task()

            if execute_task is not None:
                loop = 0

                try:
                    execute_task.run()
                except Exception as e:
                    error(self.name + ",任务执行异常！！获取新的任务执行", repr(e))
            else:
                # 没有任务可做，睡眠
                time.sleep(SLEEP_TIME)
                loop = loop + 1

        # 任务空转结束，释放自身id结束当前线程
        self.thread_pool.release_id(self.thread_id)
