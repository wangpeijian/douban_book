import random
import time

import requests
from lxml import etree

from core.const import USER_AGENTS
from repertory.proxies_address import get_proxies_ip, remove_proxies_ip, add_effective_proxies_ip
from util.url_tool import is_douban, is_xici, is_douban_list, is_douban_detail


def req_url(url):
    while True:
        proxies_ip = get_proxies_ip(url)

        # 豆瓣请求添加代理限制，必须使用代理访问
        if is_douban(url) and proxies_ip is None:
            # html = requests.get(url, headers=headers).text
            # 没有代理地址可以用，需要休眠处理，防止本地ip被封
            time.sleep(10)
            continue

        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
        }

        proxies = {}

        if proxies_ip is not None:
            proxies['https'] = proxies_ip

        try:
            html = requests.get(url, proxies=proxies, timeout=5, headers=headers).text

            dom = etree.HTML(html)

            if html.strip == "":
                remove_proxies_ip(url, proxies_ip)
                continue

            # 判断接口返回数据是否正常，错误的数据则更换代理重新拉取
            if result_has_error(url, dom, proxies_ip):
                print("=====错误的代理地址， ", proxies_ip)
                print("=====错误的html页面， ", html)
                remove_proxies_ip(url, proxies_ip)
                continue
            else:
                # 通过校验说明代理可用，加入优先级高的列表中
                add_effective_proxies_ip(proxies_ip)
                return html

        except Exception:
            print("接口请求异常，需要更换代理地址。", proxies_ip)
            # 移除错误的代理地址
            remove_proxies_ip(url, proxies_ip)


# 校验接口请求结果，判断是否是正常结果，结果不正常需要重复请求
def result_has_error(url, dom, proxies_ip):
    if is_douban(url):
        return check_douban_result(url, dom, proxies_ip)
    elif is_xici(url):
        return check_xicidaili_result(url, dom, proxies_ip)
    return False


# 校验豆瓣返回结果
def check_douban_result(url, dom, proxies_ip):
    error403 = dom.xpath('//center/h1/text()')
    # 判断接口返回数据是否正常，错误的数据则更换代理重新拉取
    if "".join(error403).find('403 Forbidden') != -1:
        print("ip被屏蔽，更换代理继续查询。", proxies_ip)
        return True

    # 校验列表是否查询成功
    if is_douban_list(url):
        error_list = dom.xpath('//*[@id="content"]/h1/text()')
        if "".join(error_list).find('豆瓣图书标签:') == -1:
            print("ip被屏蔽，列表查询数据异常。", proxies_ip)
            return True

    # 校验详情页面是否成功
    if is_douban_detail(url):
        title = dom.xpath('//*[@id="wrapper"]/h1/span/text()')
        if len(title) == 0:
            print("ip被屏蔽，详情页面查询数据异常。", proxies_ip)
            return True

    return False


# 校验西刺代理返回结果
def check_xicidaili_result(url, dom, proxies_ip):
    if dom is None:
        return True

    return False
