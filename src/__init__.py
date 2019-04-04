#!/usr/bin/python
# -*- coding: UTF-8 -*-
from impl.main import increment_entry

if __name__ == '__main__':
    print('作为主程序运行')
    # 默认程序入口从头爬取数据，如果使用增量方式爬取需要预置 `tag_dict_current` 数据，入口程序： increment_entry()
    # normal_entry()
    increment_entry()
else:
    print('package_src 初始化')
