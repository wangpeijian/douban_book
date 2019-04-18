# 定义日志级别
log_level = {
    'debug': False,
    'info': True,
    'error': True,
}

# 启动的工作线程数量
workers = 20

# 线程池缓存任务数
thread_pool_size = 5

# 每次加载tags的数据量
collection_tag_page_size = 5

# 代理地址，待选的ip超过max代理线程进入休眠
proxies_ip_max = 50

# 代理线程,当前代理地址数量超出最大值时,代理线程的一个休眠周期（s）
proxies_thread_cycle = 5

# 西刺代理地址n页后从第一页开始查找
proxies_page_loop = 100
