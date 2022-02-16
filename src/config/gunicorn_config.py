from src.config.common_config import SERVER_PORT, PATH

# 并行工作进程数
workers = 5

# 指定每个工作者的线程数
threads = 3

# 监听内网端口9999
bind = f"0.0.0.0:{SERVER_PORT}"

# 设置守护进程,将进程交给supervisor管理
daemon = 'true'

# 工作模式协程
# worker_class = 'gevent'

# 设置最大并发量
worker_connections = 5

# 设置进程文件目录
# pidfile = '/var/run/gunicorn.pid'

# 设置访问日志和错误信息日志路径
accesslog = f"{PATH}/log_files/gunicorn_acess.log"
errorlog = f"{PATH}/log_files/gunicorn_error.log"

# 设置日志记录水平
loglevel = 'info'


