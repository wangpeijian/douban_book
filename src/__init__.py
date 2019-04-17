#!/usr/bin/python
# -*- coding: UTF-8 -*-
from impl.main import increment_entry
from impl.proxies import scan_proxies_ip

if __name__ == '__main__':
    print('作为主程序运行')
    scan_proxies_ip()
    increment_entry()
else:
    print('package_src 初始化')
