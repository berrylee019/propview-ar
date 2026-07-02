import os
import requests
import pandas as pd
import xml.etree.ElementTree as ET

def fetch_apartment_data(service_key, lawd_cd, deal_ym):
    """
    국토교통부 아파트 실거래가 API 호출 함수
    :param service_key: 공공데이터포털에서 발급받은 인증키
    :param lawd_cd: 지역코드 (예: 11110 - 서울특별시 종로구)
    :param deal_ym: 거래년월 (예: 202605)
    """
    url = "https://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
    
    params = {
        'serviceKey': service_key,
        'LAWD_CD': lawd_cd,
        'DEAL_YMD': deal_ym
    }
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
    response = requests.get(url, params=params, headers=headers, timeout=10)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        items = []
        for item in root.findall('.//item'):
            data = {
                '아파트': item.find('아파트').text.strip(),
                '거래금액': item.find('거래금액').text.strip(),
                '전용면적': item.find('전용면적').text.strip(),
                '층': item.find('층').text.strip(),
                '년': item.find('년').text.strip(),
                '월': item.find('월').text.strip(),
                '일': item.find('일').text.strip()
            }
            items.append(data)
        return pd.DataFrame(items)
    else:
        print(f"Error: {response.status_code}")
        return None

# 사용 예시
if __name__ == "__main__":
    # 형님의 API 인증키를 여기에 입력하세요
    MY_SERVICE_KEY = os.getenv("SERVICE_KEY")
    
    # 예: 서울 종로구, 2026년 5월 데이터
    df = fetch_apartment_data(MY_SERVICE_KEY, "11110", "202605")
    
    if df is not None:
        print(df.head())
        # 나중에 데이터를 파일로 저장하거나 PropView 엔진으로 넘길 수 있습니다.
        df.to_csv("apt_data.csv", index=False, encoding='utf-8-sig')
