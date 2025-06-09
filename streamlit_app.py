import streamlit as st

st.title("서울시 상권 vs 유동인구 분석")
st.write("Streamlit 앱이 성공적으로 실행되었습니다!")
def calculate_total_traffic(df_grouped):
    """
    승차/하차 데이터를 합산하여 시간대별 유동인구를 계산합니다.
    입력은 group_subway_timezones() 함수의 출력 결과여야 합니다.
    """
    # 승차/하차 데이터를 분리
    df_board = df_grouped[df_grouped["구분"] == "승차"]
    df_alight = df_grouped[df_grouped["구분"] == "하차"]

    # 두 데이터프레임 병합
    df_merged = pd.merge(
        df_board,
        df_alight,
        on=["날짜", "역명"],
        suffixes=("_승차", "_하차")
    )

    # 시간대별 유동인구 합산
    traffic_cols = ["시간대_00~06", "시간대_06~11", "시간대_11~14",
                    "시간대_14~17", "시간대_17~21", "시간대_21~24"]

    for col in traffic_cols:
        df_merged[col + "_유동인구"] = df_merged[col + "_승차"] + df_merged[col + "_하차"]

    # 결과에서 필요한 컬럼만 선택
    result_cols = ["날짜", "역명"] + [col + "_유동인구" for col in traffic_cols]
    return df_merged[result_cols]
# 1단계: 시간대 그룹화
df_grouped = group_subway_timezones(df_subway)

# 2단계: 유동인구 계산
df_traffic = calculate_total_traffic(df_grouped)

# 결과 확인
df_traffic.head()
