path="/xiangfeng/my_stock"

rm ${path}/temp/*

cd ${path}
echo 'starting'
venv/bin/python -m src.run_files.run_select_stock
echo 'starting two'
zip -r ${path}/temp.zip ${path}/temp

echo 'starting end'
venv/bin/python -m src.run_files.run_send_mail_attachment

echo 'success'