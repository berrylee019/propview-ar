import os
import pandas as pd
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="서울시 아파트 실거래가 대시보드", page_icon="🏢", layout="wide"
)

st.title("🏢 서울시 아파트 실거래가 및 AR 프롭테크 대시보드")

# 데이터 파일 경로 설정
DATA_FILE = "apt_data.csv"

# 데이터 파일 존재 여부 확인 및 로드
if os.path.exists(DATA_FILE):
  df = pd.read_csv(DATA_FILE)

  # 결측치(NaN) 방지 및 문자열 변환
  df["아파트"] = df["아파트"].fillna("").astype(str)
  df["지역구"] = df["지역구"].fillna("").astype(str)

  # 1. 금액 데이터 숫자로 변환
  if "거래금액_num" not in df.columns:
    df["거래금액_num"] = (
        df["거래금액"].astype(str).str.replace(",", "", regex=True).astype(int)
    )

  # 2. 화면에 보여주기 좋게 컬럼 이름에 단위 명시하기
  df = df.rename(columns={"면적": "면적 (㎡)", "거래금액": "거래금액 (만원)"})

  # --- 사이드바 필터 설정 ---
  st.sidebar.header("🔍 필터 및 정렬 설정")

  # 1단계: 지역구 선택 (가장 먼저 적용)
  all_regions = sorted(df["지역구"].dropna().unique().tolist())
  selected_regions = st.sidebar.multiselect(
      "📍 지역구 선택 (복수 선택 가능)",
      options=all_regions,
      default=[],  # 비워두면 전체 지역
  )

  # 지역구 필터 적용
  if selected_regions:
    df_step1 = df[df["지역구"].isin(selected_regions)]
  else:
    df_step1 = df

  # 2단계: 정렬 기준 선택
  sort_option = st.sidebar.selectbox(
      "📊 정렬 기준",
      [
          "기본 (전체보기)",
          "거래 횟수 많은 순 (인기순)",
          "거래금액 높은순",
          "거래금액 낮은순",
          "최신 건축년도순",
      ],
  )

  # 정렬 옵션 적용 (지역구 필터가 적용된 df_step1 기준!)
  if sort_option == "거래 횟수 많은 순 (인기순)":
    apt_counts = df_step1["아파트"].value_counts().reset_index()
    apt_counts.columns = ["아파트", "거래 건수"]

    selected_apt = st.sidebar.multiselect(
        "인기 아파트 선택 (복수 선택)",
        options=apt_counts["아파트"].head(100).tolist(),
    )

    if selected_apt:
      filtered_df = df_step1[df_step1["아파트"].isin(selected_apt)]
    else:
      filtered_df = df_step1

  elif sort_option == "거래금액 높은순":
    filtered_df = df_step1.sort_values(by="거래금액_num", ascending=False)
    selected_apt = st.sidebar.multiselect(
        "아파트 직접 선택 (선택 시 해당 아파트만)", df_step1["아파트"].unique()
    )
    if selected_apt:
      filtered_df = filtered_df[filtered_df["아파트"].isin(selected_apt)]

  elif sort_option == "거래금액 낮은순":
    filtered_df = df_step1.sort_values(by="거래금액_num", ascending=True)
    selected_apt = st.sidebar.multiselect(
        "아파트 직접 선택 (선택 시 해당 아파트만)", df_step1["아파트"].unique()
    )
    if selected_apt:
      filtered_df = filtered_df[filtered_df["아파트"].isin(selected_apt)]

  elif sort_option == "최신 건축년도순":
    filtered_df = df_step1.sort_values(by="건축년도", ascending=False)
    selected_apt = st.sidebar.multiselect(
        "아파트 직접 선택 (선택 시 해당 아파트만)", df_step1["아파트"].unique()
    )
    if selected_apt:
      filtered_df = filtered_df[filtered_df["아파트"].isin(selected_apt)]

  else:  # 기본 전체보기
    selected_apt = st.sidebar.multiselect(
        "아파트 직접 선택", df_step1["아파트"].unique()
    )
    if selected_apt:
      filtered_df = df_step1[df_step1["아파트"].isin(selected_apt)]
    else:
      filtered_df = df_step1

  # --- 메인 화면 데이터 표시 ---
  st.subheader(f"📊 실거래 내역 (총 {len(filtered_df):,}건)")
  st.dataframe(filtered_df, use_container_width=True)

  # --- 차트 표시 ---
  st.subheader("📈 아파트별 거래가 통계")
  if not filtered_df.empty:
    chart_data = filtered_df.head(50).set_index("아파트")["거래금액_num"]
    st.bar_chart(chart_data)
  else:
    st.info("조건에 일치하는 데이터가 없습니다.")

else:
  st.warning(
      "데이터 파일(`apt_data.csv`)을 찾을 수 없습니다. GitHub에 파일이"
      " 업로드되었는지 확인해주세요."
  )
