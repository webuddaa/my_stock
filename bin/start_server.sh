cd /xiangfeng/my_stock

venv/bin/python query_server.py


#venv/bin/gunicorn -c gunicorn.conf.py src.run_files.query_server:app