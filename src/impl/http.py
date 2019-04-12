import random

import requests
from lxml import etree

from core.const import USER_AGENTS
from impl.proxies import get_proxies_ip, remove_proxies_ip, add_effective_proxies_ip


def req_url(url):
    while True:
        headers = {

            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
        }
        proxies_ip = get_proxies_ip()
        proxies = {'https': proxies_ip}
        # , proxies=proxies, timeout=2, headers=headers
        try:
            if proxies_ip is None:
                html = requests.get(url, headers=headers).text
            else:
                html = requests.get(url, proxies=proxies, timeout=2, headers=headers).text

            dom = etree.HTML(html)
            # 扫描相关的标签并记录
            error403 = dom.xpath('//center/h1/text()')

            # 判断接口返回数据是否正常，错误的数据则更换代理重新拉取
            if len(error403) > 0 and error403[0] == '403 Forbidden':
                print("ip被屏蔽，更换代理继续查询,", proxies_ip)
                # 移除错误的代理地址
                remove_proxies_ip(proxies_ip)
                pass
            else:
                # 通过校验说明代理可用，加入优先级高的列表中
                add_effective_proxies_ip(proxies_ip)
                return html

        except Exception:
            print("接口请求异常，需要更换代理地址,", proxies_ip)
            # 移除错误的代理地址
            remove_proxies_ip(proxies_ip)
