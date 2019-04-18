import threading

from core import worker_thread
from util.logger import info


# 缓存线程池
class ThreadExecute:
    def __init__(self, thread_size, task_size):
        self.thread_size = thread_size

        # 任务队列锁
        self.task_lock = threading.Lock()
        # 待执行任务的队列
        self.execute_task = []
        # 最大任务存储数量
        self.task_size = task_size

        # 获取、释放线程时加锁
        self.thread_Lock = threading.Lock()
        # 运行中的线程编号
        self.running_thread_no = []
        # 空闲中的线程编号
        self.free_thread_no = []

        # 线程队列阻塞控制
        self.execute_blocker = threading.Event()

        self.__init_thread_num__()

    def __init_thread_num__(self):
        # 根据线程池大小初始化线程编号
        i = 1
        while i <= self.thread_size:
            self.free_thread_no.append(i)
            i = i + 1

    # 获取一个空闲的线程编号
    def fetch_id(self):
        self.thread_Lock.acquire()

        # 判断空闲队列是否有可用id
        if len(self.free_thread_no) <= 0:
            self.thread_Lock.release()
            return None, False

        thread_id = self.free_thread_no.pop(0)
        self.running_thread_no.append(thread_id)
        self.thread_Lock.release()
        return thread_id, True

    # 线程结束释放一个id
    def release_id(self, thread_id):
        self.thread_Lock.acquire()
        self.free_thread_no.append(thread_id)
        self.running_thread_no.remove(thread_id)
        self.thread_Lock.release()

    # 待执行任务队列增加一个任务
    def add_task(self, execute):
        self.task_lock.acquire()
        self.execute_task.append(execute)
        self.task_lock.release()

    # 从待执行任务队列中获取一个任务
    def take_task(self):
        self.task_lock.acquire()

        if len(self.execute_task) <= 0:
            self.task_lock.release()
            return None

        task = self.execute_task.pop(0)
        self.task_lock.release()

        # 可以添加新任务，唤醒添加任务
        self.execute_blocker.set()
        self.execute_blocker.clear()

        return task

    # 添加一条工作线程
    def add_worker(self, thread_id):
        worker = worker_thread.Worker(thread_id, self)
        worker.start()

    # 添加一个任务
    def submit(self, execute):
        # 将任务加入等待队列
        self.add_task(execute)

        # 获取一个空闲线程
        thread_id, has_worker = self.fetch_id()

        # 如果有空闲线程则开启一个新线程
        if has_worker:
            self.add_worker(thread_id)

        while len(self.execute_task) >= self.task_size:
            info("任务队列超出限制，阻塞:", len(self.execute_task), self.task_size)
            self.execute_blocker.wait()
