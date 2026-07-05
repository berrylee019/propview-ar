@echo off
echo [1/2] 아파트 실거래 데이터 수집 시작...
python src/api/fetch_data.py

echo [2/2] 변경 사항 저장 및 서버 동기화...
git add apt_data.csv
git commit -m "Auto-update data: %date% %time%"
git push origin main

echo 모든 작업이 완료되었습니다!
pause
