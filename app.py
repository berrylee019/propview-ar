import streamlit as st
import pandas as pd
import os
import urllib.request
import urllib.parse

def fetch_apartment_data_robust(service_key, lawd_cd, deal_ym):
    base_url = "https://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
    params = {'serviceKey': service_key, 'LAWD_CD': lawd_cd, 'DEAL_YMD': deal_ym}
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

# 현재 경로에 어떤 파일이 있는지 출력해서 디버깅
#st.write("현재 경로 파일 리스트:", os.listdir('.'))

# 페이지 설정
st.set_page_config(page_title="PropView - 아파트 실거래가", layout="wide")

st.title("🏠 PropView: 아파트 실거래가 모니터링")
st.markdown("수집된 부동산 데이터를 실시간으로 확인합니다.")

# 데이터 파일 로드
DATA_FILE = "apt_data.csv"
df = pd.read_csv('apt_data.csv')

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    
    # 1. 사이드바 필터
    st.sidebar.header("필터 설정")
    selected_apt = st.sidebar.multiselect("아파트 선택", df['아파트'].unique())

    # 사이드바 또는 상단에 정렬 기준 선택 옵션 추가
    sort_option = st.selectbox(
        '📊 정렬 및 인기순 필터 선택',
        ['거래 횟수 많은 순 (인기순)', '최신 건축년도순', '거래금액 높은순', '거래금액 낮은순']
    )

    if sort_option == '거래 횟수 많은 순 (인기순)':
        # 아파트 이름별 거래 건수를 계산해서 인기순으로 정렬
        apt_counts = df['아파트'].value_counts().reset_index()
        apt_counts.columns = ['아파트', '거래 건수']
        
        # 상위 인기 아파트 목록을 멀티셀렉트나 셀렉박스로 연동
        selected_apt = st.multiselect(
            '인기 아파트 선택 (복수 선택 가능)', 
            options=apt_counts['아파트'].head(50).tolist(),
            default=[apt_counts['아파트'].iloc[0]]  # 기본값으로 1위 아파트 지정
        )
        filtered_df = df[df['아파트'] == selected_apt]
    
    elif sort_option == '거래금액 높은순':
        filtered_df = df.sort_values(by='거래금액', ascending=False)
    else:
        filtered_df = df
    
    # 데이터 필터링
    if selected_apt:
        filtered_df = df[df['아파트'].isin(selected_apt)]
    else:
        filtered_df = df
    
    # 2. 메인 화면 데이터 표시
    st.subheader("최근 실거래 내역")
    st.dataframe(df, use_container_width=True)
    
    # 화면에 데이터 및 차트 표시
    st.dataframe(filtered_df)

    # 3. 간단한 차트 (가격 통계)
    st.subheader("아파트별 거래가 통계")
    # 금액 데이터 전처리 (콤마 제거 및 숫자로 변환)
    df['거래금액_num'] = df['거래금액'].replace(',', '', regex=True).astype(int)
    st.bar_chart(df.set_index('아파트')['거래금액_num'])

else:
    st.warning("데이터 파일(`apt_data.csv`)을 찾을 수 없습니다. GitHub Actions가 실행되었는지 확인해주세요.")
