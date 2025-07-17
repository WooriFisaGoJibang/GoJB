import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np
import koreanize_matplotlib
from matplotlib.patches import Patch

# adjustText 설치가 필요합니다: 터미널에서 'pip install adjustText'
from adjustText import adjust_text

st.set_page_config(page_title="방문자수·문화자원수 도/광역시별 시각화", layout="wide")
st.title("📊 광역지자체별 방문자수 & 문화자원수(근대문화유산+축제) 비교")

# ======= 1. 도/광역시 표준명 매핑 =======
standard_names_map = {
    "강원도": "강원도", "강원특별자치도": "강원도",
    "경기도": "경기도",
    "경상남도": "경상남도",
    "경상북도": "경상북도",
    "광주광역시": "광주광역시",
    "대구광역시": "대구광역시",
    "대전광역시": "대전광역시",
    "부산광역시": "부산광역시",
    "서울특별시": "서울특별시", "서울시": "서울특별시",
    "세종특별자치시": "세종특별자치시",
    "울산광역시": "울산광역시",
    "인천광역시": "인천광역시",
    "전라남도": "전라남도",
    "전라북도": "전라북도", "전북특별자치도": "전라북도",
    "제주도": "제주도", "제주특별자치도": "제주도",
    "충청남도": "충청남도",
    "충청북도": "충청북도"
}
def standardize_province(name):
    if pd.isna(name):
        return None
    return standard_names_map.get(str(name).strip(), name)

# ======= 2. 근대문화유산 데이터 전처리 =======
try:
    df_heritage = pd.read_csv("data/KF_AREA_CLTUR_MDRN_CLTUR_HRITG_DATA_LIST_202312.csv", encoding='utf-8')
except UnicodeDecodeError:
    df_heritage = pd.read_csv("data/KF_AREA_CLTUR_MDRN_CLTUR_HRITG_DATA_LIST_202312.csv", encoding='cp949')
df_heritage = df_heritage.dropna(subset=['CTPRVN_NM', 'CTLSTT_LA', 'CTLSTT_LO'])
df_heritage = df_heritage.drop_duplicates(subset=['CTLSTT_LA', 'CTLSTT_LO'], keep='first')
df_heritage["CTPRVN_NM_std"] = df_heritage["CTPRVN_NM"].apply(standardize_province)
heritage_count = df_heritage.groupby('CTPRVN_NM_std')['DATA_MANAGE_NO'].count()

# ======= 3. 지역문화축제 데이터 전처리 =======
def extract_province(address):
    if pd.isna(address):
        return None
    return str(address).split()[0]
try:
    df_festival = pd.read_csv('data/전국문화축제표준데이터.csv', encoding='utf-8')
except UnicodeDecodeError:
    df_festival = pd.read_csv('data/전국문화축제표준데이터.csv', encoding='cp949')
df_festival = df_festival.dropna(subset=['위도', '경도'])
df_festival = df_festival[df_festival['위도'] != 0]
df_festival["시도명"] = df_festival["소재지도로명주소"].apply(extract_province)
df_festival["시도명_std"] = df_festival["시도명"].apply(standardize_province)
festival_count = df_festival.groupby('시도명_std')['축제명'].count()

# ======= 4. 도/광역시 기준 통합 집계 =======
all_regions = heritage_count.index.union(festival_count.index)
heritage_count_full = heritage_count.reindex(all_regions).fillna(0)
festival_count_full = festival_count.reindex(all_regions).fillna(0)
cultural_resources = heritage_count_full + festival_count_full
df_resources = pd.DataFrame({
    "광역지자체명": all_regions,
    "근대문화유산 수": heritage_count_full.values,
    "지역축제 수": festival_count_full.values,
    "문화자원수": cultural_resources.values
}).reset_index(drop=True)

# ======= 5. 방문자 데이터 전처리/표준화 =======
try:
    df_visitors = pd.read_csv("data/광역별방문자수.csv", encoding='utf-8')
except UnicodeDecodeError:
    df_visitors = pd.read_csv("data/광역별방문자수.csv", encoding='cp949')
df_visitors["광역지자체명_std"] = df_visitors["광역지자체명"].apply(standardize_province)
if "광역지자체 방문자 수" in df_visitors.columns:
    df_visitors_unique = df_visitors[['광역지자체명_std', '광역지자체 방문자 수']].drop_duplicates(subset=['광역지자체명_std'])
else:
    df_visitors_unique = df_visitors.groupby('광역지자체명_std')['기초지자체 방문자 수'].sum().reset_index()
    df_visitors_unique = df_visitors_unique.rename(columns={'기초지자체 방문자 수': '광역지자체 방문자 수'})

# ======= 6. 데이터 병합 =======
df = pd.merge(df_resources, df_visitors_unique, left_on="광역지자체명", right_on="광역지자체명_std", how="inner")

# ======= 1️⃣ 산점도 - adjustText 활용 =======
st.header("1️⃣ 산점도: 문화자원수(근대문화유산+축제) vs 방문자수")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=df, x="문화자원수", y="광역지자체 방문자 수", s=90, ax=ax)
X = df["문화자원수"].values.reshape(-1, 1)
y = df["광역지자체 방문자 수"].values
model = LinearRegression().fit(X, y)
x_vals = np.linspace(df["문화자원수"].min(), df["문화자원수"].max(), 100)
y_vals = model.predict(x_vals.reshape(-1, 1))
ax.plot(x_vals, y_vals, color="red", linestyle="--", label="회귀선")
# 라벨 겹침 방지: adjustText 사용
texts = []
for i, row in df.iterrows():
    texts.append(
        ax.text(row["문화자원수"], row["광역지자체 방문자 수"], row["광역지자체명"], fontsize=9)
    )
adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="-", color='gray', lw=0.5))

ax.set_xlabel("문화자원 수 (근대문화유산 + 지역축제 개수)")
ax.set_ylabel("광역지자체 방문자 수")
ax.set_title("문화자원 수가 많을수록 방문자수도 많다")
ax.legend()
st.pyplot(fig)

# ======= 2️⃣ 도/광역시 단위 이중 y축 막대그래프 (범례 색상 Patch 적용) =======
st.header("2️⃣ 광역지자체별 방문자수 & 문화자원수 이중 y축 그래프")
df_sorted = df.sort_values("광역지자체 방문자 수", ascending=False).reset_index(drop=True)
bar_width = 0.45
x = np.arange(len(df_sorted))

fig2, ax1 = plt.subplots(figsize=(12, 7))
bars1 = ax1.bar(x - bar_width/2, df_sorted["광역지자체 방문자 수"], bar_width, label="방문자수(명)", color='tab:blue')
ax1.set_ylabel("방문자수(명)", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 두 번째 y축 - 문화자원수 : 정규화 (최대값 기준)
ax2 = ax1.twinx()
norm_cultural = df_sorted["문화자원수"] / df_sorted["문화자원수"].max() * df_sorted["광역지자체 방문자 수"].max()
bars2 = ax2.bar(x + bar_width/2, norm_cultural, bar_width, label="문화자원수 (정규화)", color='tab:orange', alpha=0.7)
ax2.set_ylabel("문화자원수 (정규화, 최대 방문자수 기준)", color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.set_xticks(x)
ax1.set_xticklabels(df_sorted["광역지자체명"], rotation=45)
ax1.set_title("광역지자체별 방문자수·문화자원수 이중 y축 비교")

# 범례(legend) 패치로 색상 명확하게 표기
legend_patches = [
    Patch(facecolor='tab:blue', label='방문자수(명)'),
    Patch(facecolor='tab:orange', label='문화자원수 (정규화)')
]
ax1.legend(handles=legend_patches, loc='upper right')

st.pyplot(fig2)

with st.expander("🔍 데이터 미리보기"):
    st.dataframe(df)
