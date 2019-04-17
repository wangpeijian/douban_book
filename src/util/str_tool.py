# 处理图书标签，书名的特殊字符
def escape_str(string):
    string = string.replace('\"', '\\"')
    string = string.replace('\'', "\\'")
    string = string.replace('\\', "\\\\")
    return string
