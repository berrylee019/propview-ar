import streamlit as st
import pandas as pd
import os

# 현재 경로에 어떤 파일이 있는지 출력해서 디버깅
st.write("현재 경로 파일 리스트:", os.listdir('.'))

# 페이지 설정
st.set_page_config(page_title="PropView - 아파트 실거래가", layout="wide")

st.title("🏠 PropView: 아파트 실거래가 모니터링")
st.markdown("수집된 부동산 데이터를 실시간으로 확인합니다.")

# 데이터 파일 로드
DATA_FILE = "apt_data.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    
    # 1. 사이드바 필터
    st.sidebar.header("필터 설정")
    selected_apt = st.sidebar.multiselect("아파트 선택", df['아파트'].unique())
    
    # 데이터 필터링
    if selected_apt:
        df = df[df['아파트'].isin(selected_apt)]
    
    # 2. 메인 화면 데이터 표시
    st.subheader("최근 실거래 내역")
    st.dataframe(df, use_container_width=True)
    
    # 3. 간단한 차트 (가격 통계)
    st.subheader("아파트별 거래가 통계")
    # 금액 데이터 전처리 (콤마 제거 및 숫자로 변환)
    df['거래금액_num'] = df['거래금액'].replace(',', '', regex=True).astype(int)
    st.bar_chart(df.set_index('아파트')['거래금액_num'])

else:
    st.warning("데이터 파일(`apt_data.csv`)을 찾을 수 없습니다. GitHub Actions가 실행되었는지 확인해주세요.")
