# 处理图书标签，书名的特殊字符
def escape_str(string):
    string = string.replace('\\', "\\\\")
    string = string.replace('\"', '\\"')
    string = string.replace('\'', "\\'")
    return string


# 请求链接中的字符串处理
def escape_url(string):
    string = string.replace('/', "%E2%88%95")
    return string
