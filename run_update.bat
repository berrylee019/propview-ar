@echo off
echo [1/3] 데이터 수집 시작...
python src\api\fetch_data.py

echo [2/3] 변경 사항 확인 및 커밋...
git add apt_data.csv
git commit -m "Auto-update data: %date% %time%"

echo [3/3] 서버로 데이터 전송...
git push origin main

echo 작업 완료! 대시보드에서 확인해 보세요.
pause
