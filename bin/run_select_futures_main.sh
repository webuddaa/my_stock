cd /xiangfeng/my_stock

cat /dev/null > ./log_files/run_select_futures.log
cat /dev/null > ./log_files/gunicorn_acess.log

period_list='["day","60","30","15","5","1"]'

venv/bin/python -m src.futures.run_select_futures --period_list ${period_list}


# nohup ./run_select_futures_temp.sh > aa.log 2>&1 &

# 5 2 * * * /xiangfeng/my_stock/bin/run_select_futures_main.sh > /xiangfeng/my_stock/bin/aa.log 2>&1 &
# 16 10 * * * /xiangfeng/my_stock/bin/run_select_futures_temp.sh > /xiangfeng/my_stock/bin/aa.log 2>&1 &
# 32 11 * * * /xiangfeng/my_stock/bin/run_select_futures_main.sh > /xiangfeng/my_stock/bin/aa.log 2>&1 &
# 5 15 * * * /xiangfeng/my_stock/bin/run_select_futures_main.sh > /xiangfeng/my_stock/bin/aa.log 2>&1 &
