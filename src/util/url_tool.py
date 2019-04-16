def is_douban(url):
    return url.find("douban") != -1


def is_douban_list(url):
    return url.find('https://book.douban.com/tag/') != -1 and url.find('?start=') != -1 and url.find('&type=T') != -1


def is_douban_detail(url):
    return url.find('https://book.douban.com/subject/') != -1


def is_xici(url):
    return url.find("xicidaili") != -1
