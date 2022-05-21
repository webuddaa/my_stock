cd /xiangfeng/my_stock

venv/bin/python query_server.py


#venv/bin/gunicorn -c src/config/gunicorn_config.py src.run_files.query_server:app