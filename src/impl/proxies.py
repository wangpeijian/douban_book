import random
import threading
import time

from lxml import etree

from core.const import USER_AGENTS
from impl import http

# 记录全部代理地址
PROXIES_IP = []

# 记录执行成功过的代理地址，获取地址时优先从成功过的地址获取
EFFECTIVE_PROXIES_IP = []


def remove_proxies_ip(proxies_ip):
    if proxies_ip in EFFECTIVE_PROXIES_IP:
        EFFECTIVE_PROXIES_IP.remove(proxies_ip)

    if proxies_ip in PROXIES_IP:
        PROXIES_IP.remove(proxies_ip)


def get_proxies_ip():
    if len(EFFECTIVE_PROXIES_IP) > 0:
        return random.choice(EFFECTIVE_PROXIES_IP)

    if len(PROXIES_IP) > 0:
        return random.choice(PROXIES_IP)

    return None


def add_proxies_ip(proxies_ip):
    PROXIES_IP.append(proxies_ip)


def add_effective_proxies_ip(proxies_ip):
    EFFECTIVE_PROXIES_IP.append(proxies_ip)


def async_do(thread_name, sleep_time):
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }

    i = 1
    while True:

        # 如果当前代理地址过多则空转
        if len(PROXIES_IP) > 50 or len(EFFECTIVE_PROXIES_IP) > 3:
            time.sleep(sleep_time)
            pass

        i = i + 1
        url = 'https://www.xicidaili.com/wn/%s' % i
        print(thread_name + ":" + url)
        html = http.req_url(url)

        dom = etree.HTML(html)

        print("==========", html)

        # 扫描相关的标签并记录
        lines = dom.xpath('//*[@id="ip_list"]/tr')

        for item in lines:
            tds = item.xpath('./td/text()')
            if len(tds) != 0:
                add_proxies_ip(tds[0] + ":" + tds[1])

        time.sleep(sleep_time)
        pass


# 爬取代理的ip地址
def scan_proxies_ip(sleep_time):
    try:
        proxies_thread = threading.Thread(target=async_do, args=("Thread-proxies_ip", sleep_time,))
        proxies_thread.start()
    except Exception:
        scan_proxies_ip(sleep_time)
