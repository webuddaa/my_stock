cd /xiangfeng/my_stock

cat /dev/null > ./log_files/run_select_futures.log
cat /dev/null > ./log_files/gunicorn_acess.log

period_list='["5","1"]'

venv/bin/python -m src.futures.run_select_futures --period_list ${period_list}


# nohup ./run_select_futures_temp.sh > aa.log 2>&1 &