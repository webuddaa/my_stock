cd /xiangfeng/my_stock

cat /dev/null > ./log_files/run_select_futures.log
cat /dev/null > ./log_files/gunicorn_acess.log

venv/bin/python -m src.futures.run_select_futures


#nohup ./run_select_futures.sh > aa.log 2>&1 &