import threading
import time

from lxml import etree

from config.system import proxies_thread_cycle
from core.blocker import wake_up_worker
from impl import http
from repertory.proxies_address import PROXIES_IP, add_proxies_ip
from util.logger import log


def async_do():
    i = 1
    while True:
        # 如果当前代理地址过多则空转
        log("待选的ip地址数量:", len(PROXIES_IP))
        if len(PROXIES_IP) > 50:
            time.sleep(proxies_thread_cycle)
            continue

        url = 'https://www.xicidaili.com/wn/%s' % i
        log(url)
        html = http.req_url(url)
        dom = etree.HTML(html)

        try:
            log("代理地址拉取成功，准备解析")
            # 扫描相关的标签并记录
            lines = dom.xpath('//*[@id="ip_list"]/tr')

            for item in lines:
                tds = item.xpath('./td/text()')
                if len(tds) != 0:
                    add_proxies_ip(tds[0] + ":" + tds[1])

            log("拉取新的ip地址后，待选的ip地址数量:", len(PROXIES_IP))
            # 加入新的代理地址唤醒工作线程
            wake_up_worker()

            # 代理地址翻页数量过多，则重第一页开始扫描
            i = i + 1
            if i > 1000:
                i = 1

        except Exception as e:
            log("解析西刺代理页面异常：", repr(e), html)
            continue


# 爬取代理的ip地址
def scan_proxies_ip():
    try:
        proxies_thread = threading.Thread(target=async_do)
        proxies_thread.setName("Thread-proxies_ip")
        proxies_thread.start()
    except Exception as e:
        log("代理扫描任务异常：", repr(e))
        scan_proxies_ip()
