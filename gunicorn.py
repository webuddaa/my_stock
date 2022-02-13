# 并行工作进程数
workers = 2

# 指定每个工作者的线程数
threads = 2

# 监听内网端口9999
bind = '47.94.99.97:9999'

# 设置守护进程,将进程交给supervisor管理
daemon = 'false'

# 工作模式协程
# worker_class = 'gevent'

# 设置最大并发量
# worker_connections = 2000

# 设置进程文件目录
# pidfile = '/var/run/gunicorn.pid'

# 设置访问日志和错误信息日志路径
accesslog = './log_files/gunicorn_acess.log'
errorlog = './log_files/gunicorn_error.log'


