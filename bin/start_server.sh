path="/xiangfeng/my_stock"

cd ${path}

venv/bin/python -m src.run_files.query_server


#venv/bin/gunicorn -c src/config/gunicorn_config.py src.run_files.query_server:app