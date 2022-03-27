path="/xiangfeng/my_stock"

rm ${path}/static/*

cd ${path}

venv/bin/python -m src.run_files.run_select_stock
