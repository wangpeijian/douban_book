import threading

from impl import main
from impl import mysql


class LoadThread(threading.Thread):
    def __init__(self, tag, page_start, pool):
        threading.Thread.__init__(self)

        thread_id = pool.fetch_id()

        self.thread_id = thread_id
        self.name = "线程-%s" % thread_id
        self.tag = tag
        self.page_start = page_start
        self.pool = pool

    def run(self):
        main.load_tag(self.tag, self.page_start)
        # 更新tag状态,tag标记为完成状态
        mysql.update_tag_done(self.tag)
        self.pool.release_id(self.thread_id)
