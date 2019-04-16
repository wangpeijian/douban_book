import random

from util.logger import log
from util.url_tool import is_douban, is_xici

# 记录全部代理地址
PROXIES_IP = []

# 记录执行成功过的代理地址，获取地址时优先从成功过的地址获取
EFFECTIVE_PROXIES_IP = []

# 记录豆瓣接口可使用的代理地址，豆瓣使用的代理地址和西刺的代理地址可能屏蔽的不一致，防止删掉能用的代理地址
EFFECTIVE_PROXIES_IP_DOU_BAN = ['121.40.78.138:3128']


def remove_proxies_ip(url, proxies_ip):
    # 豆瓣屏蔽
    if is_douban(url):
        if proxies_ip in EFFECTIVE_PROXIES_IP_DOU_BAN:
            EFFECTIVE_PROXIES_IP_DOU_BAN.remove(proxies_ip)

    # 西刺屏蔽
    if is_xici(url):
        if proxies_ip in EFFECTIVE_PROXIES_IP:
            EFFECTIVE_PROXIES_IP.remove(proxies_ip)

    if proxies_ip in PROXIES_IP:
        PROXIES_IP.remove(proxies_ip)


def get_proxies_ip(url):
    # 豆瓣获取
    if is_douban(url):
        if len(EFFECTIVE_PROXIES_IP_DOU_BAN) > 0:
            return random.choice(EFFECTIVE_PROXIES_IP_DOU_BAN)

    # 西刺获取
    if is_xici(url):
        if len(EFFECTIVE_PROXIES_IP) > 0:
            return random.choice(EFFECTIVE_PROXIES_IP)

    if len(PROXIES_IP) > 0:
        return random.choice(PROXIES_IP)

    log("没有可用的代理地址了")
    return None


def add_proxies_ip(proxies_ip):
    if proxies_ip is None:
        return

    if proxies_ip not in PROXIES_IP:
        PROXIES_IP.append(proxies_ip)


def add_effective_proxies_ip(proxies_ip):
    if proxies_ip is None:
        return

    if proxies_ip not in EFFECTIVE_PROXIES_IP_DOU_BAN:
        EFFECTIVE_PROXIES_IP_DOU_BAN.append(proxies_ip)
        log("豆瓣,发现可用代理地址：", proxies_ip)

    if proxies_ip not in EFFECTIVE_PROXIES_IP:
        EFFECTIVE_PROXIES_IP.append(proxies_ip)
        log("西刺,发现可用代理地址：", proxies_ip)
