rm run_files/src.zip

zip -r run_files/src.zip src

git add -A .

git commit -m "优化日志"

git push origin feature-v1
