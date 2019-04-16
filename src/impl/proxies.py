import threading
import time

from lxml import etree

from impl import http
from repertory.proxies_address import PROXIES_IP, EFFECTIVE_PROXIES_IP_DOU_BAN, add_proxies_ip


def async_do(thread_name, sleep_time):
    i = 1
    while True:
        # 如果当前代理地址过多则空转
        if len(PROXIES_IP) > 250 or len(EFFECTIVE_PROXIES_IP_DOU_BAN) > 3:
            time.sleep(sleep_time)
            continue

        url = 'https://www.xicidaili.com/wn/%s' % i
        print(thread_name + ":" + url)
        html = http.req_url(url)
        dom = etree.HTML(html)

        try:
            # 扫描相关的标签并记录
            lines = dom.xpath('//*[@id="ip_list"]/tr')

            for item in lines:
                tds = item.xpath('./td/text()')
                if len(tds) != 0:
                    add_proxies_ip(tds[0] + ":" + tds[1])
            print("待选的ip地址数量:", len(PROXIES_IP))
            i = i + 1
        except Exception:
            print("解析西刺代理页面异常：======", html, dom)
            continue


# 爬取代理的ip地址
def scan_proxies_ip(sleep_time):
    try:
        proxies_thread = threading.Thread(target=async_do, args=("Thread-proxies_ip", sleep_time,))
        proxies_thread.start()
    except Exception:
        scan_proxies_ip(sleep_time)
