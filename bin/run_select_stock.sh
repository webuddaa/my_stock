path="/xiangfeng/my_stock"

zip -r ${path}/run_files/src.zip ${path}/src

cd ${path}/run_files

unzip src.zip

/xiangfeng/my_stock/venv/bin/python ${path}/run_files/run_select_stock.py --path ${path}

rm -rf ${path}/run_files/src
rm