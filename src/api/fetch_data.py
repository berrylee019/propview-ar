import os
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# .env 파일 읽어오기
load_dotenv()

def fetch_seoul_apartment_data(service_key):
    # 서울시 부동산 실거래가 정보 API 엔드포인트 (예시: 신청하신 서비스 규격에 맞춤)
    # 서울시 Open API는 보통 인증키가 URL 경로에 포함됩니다.
    url = f"http://openAPI.seoul.go.kr:8088/{service_key}/json/tbLnOaOpenStndrd/1/1000/"
    
    print(f"서울시 API 요청 중: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 서울시 API 응답 구조에 따른 데이터 추출
        if "tbLnOaOpenStndrd" in data:
            rows = data["tbLnOaOpenStndrd"]["row"]
            df = pd.DataFrame(rows)
            return df
        else:
            print("데이터 구조를 확인해주세요:", data)
            return None
            
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

if __name__ == "__main__":
    # 방금 발급받으신 서울시 인증키를 여기에 넣으세요!
    MY_SERVICE_KEY = os.getenv("SERVICE_KEY")
    
    
    if not MY_SERVICE_KEY:
        print("경고: 인증키를 찾을 수 없습니다. .env 파일을 확인해주세요.")
    else:
        df = fetch_seoul_apartment_data(MY_SERVICE_KEY)
        
        if df is not None and not df.empty:
            df.to_csv("apt_data.csv", index=False, encoding="utf-8-sig")
            print("데이터 저장 성공: apt_data.csv")
        else:
            print("데이터 수집 실패...")
