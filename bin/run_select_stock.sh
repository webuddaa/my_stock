path="/xiangfeng/my_stock"

rm ${path}/temp/*

cd ${path}

venv/bin/python -m src.run_files.run_select_stock
