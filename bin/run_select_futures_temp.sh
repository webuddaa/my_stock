cd /xiangfeng/my_stock

cat /dev/null > ./log_files/run_select_futures.log
cat /dev/null > ./log_files/gunicorn_acess.log

period_list='["1","5"]'

venv/bin/python -m src.futures.run_select_futures --period_list ${period_list}
