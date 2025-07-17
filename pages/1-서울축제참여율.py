import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

try:
    seoul = pd.read_csv(r"./data/서울축제참여율및만족도(2005년이후).csv", encoding='utf-8')
except UnicodeDecodeError:
    seoul = pd.read_csv(r"./data/서울축제참여율및만족도(2005년이후).csv")

# --------------------------------------------------------------------------------------------
# <데이터 전처리>

# 연령별, 혼인상태별, 성별만 남기기
seoul = seoul[seoul['구분별(2)'].isin(['연령별', '혼인상태별', '성별'])].copy()

# 참여경험만 남기기
seoul = seoul[seoul['만족도별(1)'].isin(['서울축제 참여 만족도', '서울축제 참여 경험'])].copy()

# 열 삭제
seoul = seoul.drop(columns=['구분별(1)']).reset_index(drop=True)

# 결측치 처리
seoul.loc[72, '2012']  = str(round(100-20.8-56.0-22.3-0.8, 4))

# 2010, 2012, 2014 자료형을 float으로 변경
seoul['2010'] = seoul['2010'].astype(float)
seoul['2012'] = seoul['2012'].astype(float)
seoul['2014'] = seoul['2014'].astype(float)

# 변수명 변경
seoul = seoul.rename(columns={
    '구분별(2)': '대분류',
    '구분별(3)': '소분류',
    '만족도별(1)': '만족도분류',
    '만족도별(2)': '만족도'
})

seoul_experience = seoul[seoul['만족도분류'] == '서울축제 참여 경험'][['대분류', '소분류', '만족도', '2010', '2012', '2014']].copy().reset_index(drop=True)

st.markdown("<h3>서울 축제 참여 경험 비율</h3>", unsafe_allow_html=True)
st.dataframe(seoul_experience)
st.markdown("<br><br>", unsafe_allow_html=True)  # 두 줄 공백

# --------------------------------------------------------------------------------------------
# <성별에 따른 서울 축제 참여 경험 비율>

gender_experience = seoul_experience[seoul_experience['대분류'] == '성별']

# Streamlit 제목
st.markdown("<h3>성별에 따른 서울 축제 참여 경험 비율(2014)</h3>", unsafe_allow_html=True)


# 남자와 여자 각각의 데이터 추출
male_data = gender_experience[gender_experience['소분류'] == '남자']
female_data = gender_experience[gender_experience['소분류'] == '여자']

# 서브플롯 생성
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# 남자 파이 차트
axes[0].pie(male_data['2014'], labels=male_data['만족도'], autopct='%1.1f%%',
            startangle=90, colors=['lightcoral', 'lightskyblue'])
axes[0].set_title('남자')

# 여자 파이 차트
axes[1].pie(female_data['2014'], labels=female_data['만족도'], autopct='%1.1f%%',
            startangle=90, colors=['lightcoral', 'lightskyblue'])
axes[1].set_title('여자')

# 레이아웃 조정 후 Streamlit에 출력
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
st.pyplot(fig)
st.markdown("<br><br>", unsafe_allow_html=True)  # 두 줄 공백

# --------------------------------------------------------------------------------------------
# <연령대에 따른 서울 축제 참여 경험 비율>

st.markdown("<h3>연령별 서울 축제 참여 경험 비율(2014)</h3>", unsafe_allow_html=True)

# 연령별 데이터 필터링
age_experience = seoul_experience[seoul_experience['대분류'] == '연령별']
age_groups = age_experience['소분류'].unique()

# 서브플롯 구성
n_cols = 3
n_rows = (len(age_groups) + n_cols - 1) // n_cols
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 5))

# 2D → 1D 축 배열 평탄화
axes = axes.flatten()

# 각 연령대별 파이 차트 그리기
for i, age_group in enumerate(age_groups):
    age_data = age_experience[age_experience['소분류'] == age_group]
    axes[i].pie(
        age_data['2014'],
        labels=age_data['만족도'],
        autopct='%1.1f%%',
        startangle=90,
        colors=['lightcoral', 'lightskyblue']
    )
    axes[i].set_title(age_group)

# 남은 subplot 제거 (빈 칸)
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# 레이아웃 정리 및 출력
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
st.pyplot(fig)
st.markdown("<br><br>", unsafe_allow_html=True)  # 두 줄 공백

# --------------------------------------------------------------------------------------------
# <혼인상태에 따른 서울 축제 참여 경험 비율>

st.markdown("<h3>혼인 상태별 서울 축제 참여 경험 비율(2014)</h3>", unsafe_allow_html=True)

# 혼인 상태별 데이터 필터링
marital_experience = seoul_experience[seoul_experience['대분류'] == '혼인상태별']
marital_groups = marital_experience['소분류'].unique()

# 서브플롯 설정
n_cols = 2
n_rows = (len(marital_groups) + n_cols - 1) // n_cols
fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, n_rows * 6))
axes = axes.flatten()  # 2D → 1D

# 파이 차트 생성
for i, marital_group in enumerate(marital_groups):
    marital_data = marital_experience[marital_experience['소분류'] == marital_group]
    axes[i].pie(
        marital_data['2014'],
        labels=marital_data['만족도'],
        autopct='%1.1f%%',
        startangle=90,
        colors=['lightcoral', 'lightskyblue']
    )
    axes[i].set_title(marital_group)

# 남은 빈 subplot 제거
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# 레이아웃 조정 후 출력
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
st.pyplot(fig)

# --------------------------------------------------------------------------------------------
# <요약>

st.markdown("""
- 서울 축제 참여 경험은 성별보다는 **연령**과 **혼인 상태**에 따라 더 큰 차이를 보였음<br>
- 특히 **20대**와 **미혼**인 경우에 축제 참여 경험이 상대적으로 높은 경향을 보였음<br>
- **중장년층**의 참여 비율이 상대적으로 낮음
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""<p style='font-size:25px;'>
💡 문화유산과 지역 축제 등 중장년층이 즐길 수 있을만한 관광 자원을 추천하자<br>
💡 20대, 미혼 집단이 관심 가질만한 / 잘 모르고 있던 축제들을 추천하자

</p>""", unsafe_allow_html=True)