from lxml import etree

from core import const
from db import mysql
from impl import http
from util.logger import log


class Execute:

    def __init__(self, tag, page_start):
        # print('创建可执行任务任务, tag: %s, page_start: %s' % (tag, page_start))
        self.tag = tag
        self.page_start = page_start

    # 记录代办的标签列表
    @staticmethod
    def record_todo_tags(tags):
        for tag in tags:
            if not mysql.has_tag(tag):
                mysql.add_tag(tag)
                const.THREAD_EXECUTE.submit(Execute(tag, 0))

    def load_tag(self, tag, page_start):
        url = 'https://book.douban.com/tag/' + tag + '?start=' + str(page_start) + '&type=T'
        log(url)

        data = http.req_url(url)
        s = etree.HTML(data)

        # 扫描相关的标签并记录
        ref_tags = s.xpath('//*[@class="tags-list"]/a/text()')
        self.record_todo_tags(ref_tags)

        url_list = s.xpath('//*[@class="subject-item"]/div/h2/a/@href')

        log(url, "扫描到的列表数据:", url_list)

        index = 0
        for url in url_list:
            index = index + 1
            #  根据图书详情页面链接爬取 评分，常用标签，简介， 图书名称
            detail_data = http.req_url(url)
            detail_tree = etree.HTML(detail_data)

            tags = detail_tree.xpath('//*[@class="indent"]/span/a/text()')
            rating = detail_tree.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')
            title = detail_tree.xpath('//*[@id="wrapper"]/h1/span/text()')
            intro = detail_tree.xpath('//*[@class="intro"]/p/text()')

            # 记录相关标签
            self.record_todo_tags(tags)

            res = url.split("/")

            _id = res[4]
            _book_name = "".join(title).strip()
            _tags = "|".join(tags)
            _intro = "".join(intro)
            _rating = "".join(rating).strip()
            _url = url

            log(
                '图书链接：', url,
                '图书id：', _id,
                '图书名称：', _book_name,
                '图书评分：', _rating,
                '图书标签：', _tags,
                '图书简介：', _intro
            )

            # 保存图书信息
            mysql.add_book(_id, _book_name, _tags, _intro, _rating, _url)
            # 循环结束更新当前查询进度
            mysql.update_tag_start(tag, page_start + index)

        if len(url_list) != 0:
            self.load_tag(tag, page_start + 20)
        else:
            # 没有拉取到新数据说明数据获取完毕
            mysql.update_tag_done(tag)
            return

    def run(self):
        self.load_tag(self.tag, self.page_start)
