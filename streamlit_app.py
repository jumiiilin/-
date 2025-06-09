import streamlit as st

st.title("서울시 상권 vs 유동인구 분석")
st.write("Streamlit 앱이 성공적으로 실행되었습니다!")
import pandas as pd

def group_subway_timezones(df_subway):
    """
    서울교통공사 지하철 시간대 데이터를 상권 시간대 구간(6개)으로 그룹화하여 반환합니다.
    """
    # 상권 시간대 기준에 맞게 지하철 시간대 컬럼 그룹 정의
    subway_time_columns = {
        "시간대_00~06": ["06시 이전"],
        "시간대_06~11": ["06시-07시", "07시-08시", "08시-09시", "09시-10시", "10시-11시"],
        "시간대_11~14": ["11시-12시", "12시-13시", "13시-14시"],
        "시간대_14~17": ["14시-15시", "15시-16시", "16시-17시"],
        "시간대_17~21": ["17시-18시", "18시-19시", "19시-20시", "20시-21시"],
        "시간대_21~24": ["21시-22시", "22시-23시", "23시-24시"],
    }

    df_grouped = df_subway.copy()

    # 각 시간대 그룹에 대해 합산
    for new_col, time_range in subway_time_columns.items():
        df_grouped[new_col] = df_grouped[time_range].sum(axis=1)

    # 결과에 필요한 컬럼만 정리해서 반환
    grouped_cols = ["날짜", "역명", "구분"] + list(subway_time_columns.keys())
    return df_grouped[grouped_cols]
df_grouped = group_subway_timezones(df_subway)
df_grouped.head()
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
# "동대문역"이 포함된 상권만 필터링
dongdaemun_sales = df_sales[df_sales['상권_코드_명'].str.contains("동대문역", na=False)]
# "동대문역"의 유동인구 데이터만 필터링
dongdaemun_traffic = df_traffic[df_traffic["역명"] == "동대문"]
# 시간대별 평균 유동인구
dongdaemun_traffic_avg = dongdaemun_traffic.mean(numeric_only=True)

# 시간대별 평균 매출 (업종 구분 없이 전체 평균)
dongdaemun_sales_avg = dongdaemun_sales[ [col for col in dongdaemun_sales.columns if "시간대_" in col and "매출_금액" in col]].mean()
# 컬럼 이름 통일 (매출, 유동인구 모두 시간대_00~06 형식으로 정리됨)
avg_df = pd.DataFrame({ '시간대': dongdaemun_sales_avg.index.str.replace("_매출_금액", "", regex=False),'평균_매출': dongdaemun_sales_avg.values,'평균_유동인구': dongdaemun_traffic_avg.values})
correlation = avg_df['평균_매출'].corr(avg_df['평균_유동인구'])
print(f"동대문역 기준 시간대별 매출 vs 유동인구 상관계수: {correlation:.4f}")
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(avg_df['시간대'], avg_df['평균_매출'], marker='o', label='평균 매출')
plt.plot(avg_df['시간대'], avg_df['평균_유동인구'], marker='s', label='평균 유동인구')
plt.title('동대문역 시간대별 매출 vs 유동인구')
plt.xlabel('시간대')
plt.ylabel('값')
plt.legend()
plt.grid(True)
plt.show()
