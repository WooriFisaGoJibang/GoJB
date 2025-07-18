import pandas as pd
import numpy as np
# import konlpy
import matplotlib.pyplot as plt
import plotly.express as px
import koreanize_matplotlib
import streamlit as st
from PIL import Image
from wordcloud import WordCloud,STOPWORDS, ImageColorGenerator
import re

## 전처리
# 파일 불러오기
# file_path_2019 = r'./data/KC_594_WNTY_FSTV_TRND_MAP_2019.csv'
# file_path_2020 = r'./data/KC_594_WNTY_FSTV_TRND_MAP_2020.csv'
# file_path_2021 = r'./data/KC_594_WNTY_FSTV_TRND_MAP_2021.csv'
# file_path_2022 = r'./data/KC_594_WNTY_FSTV_TRND_MAP_2022.csv'
# file_path_2023 = r'./data/KC_594_WNTY_FSTV_TRND_MAP_2023.csv'


# festival19 = pd.read_csv(file_path_2019, encoding = 'utf-8')
# festival20 = pd.read_csv(file_path_2020, encoding = 'utf-8')
# festival21 = pd.read_csv(file_path_2021, encoding = 'utf-8')
# festival22 = pd.read_csv(file_path_2022, encoding = 'utf-8')
# festival23 = pd.read_csv(file_path_2023, encoding = 'utf-8')

festival19 = pd.read_csv(r'./data/KC_594_WNTY_FSTV_TRND_MAP_2019.csv', encoding = 'utf-8')
festival20 = pd.read_csv(r'./data/KC_594_WNTY_FSTV_TRND_MAP_2020.csv', encoding = 'utf-8')
festival21 = pd.read_csv(r'./data/KC_594_WNTY_FSTV_TRND_MAP_2021.csv', encoding = 'utf-8')
festival22 = pd.read_csv(r'./data/KC_594_WNTY_FSTV_TRND_MAP_2022.csv', encoding = 'utf-8')
festival23 = pd.read_csv(r'./data/KC_594_WNTY_FSTV_TRND_MAP_2023.csv', encoding = 'utf-8')

# 행 영>한 변환
new_columns = {
    'FCLTY_ID': '시설ID',
    'FCLTY_NM': '시설명',
    'LC_LA': '위치위도',
    'LC_LO': '위치경도',
    'CTPRVN_NM': '시도명',
    'SIGNGU_NM': '시군구명',
    'LEGALDONG_CD': '법정동코드',
    'LEGALDONG_NM': '법정동명',
    'ADSTRD_CD': '행정동코드',
    'ADSTRD_NM': '행정동명',
    'RDNMADR_CD': '도로명주소코드',
    'RDNMADR_NM': '도로명주소명',
    'SEARCH_MT': '검색월',
    'SEARCH_CO': '검색수',
    'RANK_CO': '순위수',
    'FILE_NM': '파일명',
    'BASE_DE': '기준일자'
}

# 실제 데이터 확인
festival19 = festival19.rename(columns=new_columns)
festival20 = festival20.rename(columns=new_columns)
festival21 = festival21.rename(columns=new_columns)
festival22 = festival22.rename(columns=new_columns)
festival23 = festival23.rename(columns=new_columns)

# 원하는 열 추출
selected_col19 = festival19[['시설명', '시도명', '검색수']]
selected_col20 = festival20[['시설명', '시도명', '검색수']]
selected_col21 = festival21[['시설명', '시도명', '검색수']]
selected_col22 = festival22[['시설명', '시도명', '검색수']]
selected_col23 = festival23[['시설명', '시도명', '검색수']]

# 검색량 추출
# 2019년
# Group by '시설명' and sum the '검색수'
grouped_festival19 = selected_col19.groupby('시설명')['검색수'].sum().reset_index()

# 2020년
# Group by '시설명' and sum the '검색수'
grouped_festival20 = selected_col20.groupby('시설명')['검색수'].sum().reset_index()

# 2021년
# Group by '시설명' and sum the '검색수'
grouped_festival21 = selected_col21.groupby('시설명')['검색수'].sum().reset_index()

# 2022년
# Group by '시설명' and sum the '검색수'
grouped_festival22 = selected_col22.groupby('시설명')['검색수'].sum().reset_index()

# 2023년
# Group by '시설명' and sum the '검색수'
grouped_festival23 = selected_col23.groupby('시설명')['검색수'].sum().reset_index()

# 검색량 전체 합
title_festival19 = grouped_festival19.sort_values(by='검색수', ascending=False).head(50)
title_festival20 = grouped_festival20.sort_values(by='검색수', ascending=False).head(50)
title_festival21 = grouped_festival21.sort_values(by='검색수', ascending=False).head(50)
title_festival22 = grouped_festival22.sort_values(by='검색수', ascending=False).head(50)
title_festival23 = grouped_festival23.sort_values(by='검색수', ascending=False).head(50)

## 연도별 시설명과 검색 수 테이블
# 연도별 랭크 리스트
ranked_top50_list = []

# Iterate through each year's top 10 dataframe and add a 'Rank' column
for year, df in [(2019, title_festival19), (2020, title_festival20), (2021, title_festival21), (2022, title_festival22), (2023, title_festival23)]:
    ranked_df = df.copy()
    ranked_df['Rank'] = range(1, len(ranked_df) + 1)
    ranked_df['Year'] = year
    ranked_top50_list.append(ranked_df)

# Concatenate the ranked dataframes
ranked_top50_all_years = pd.concat(ranked_top50_list)

# Pivot the table with Year as columns and Rank as index
pivot_table_ranked = ranked_top50_all_years.pivot_table(index='Rank', columns='Year', values='시설명', aggfunc='first')


# Function to clean the festival names
def clean_festival_name(name):
    # Remove "제n회 " (e.g., 제24회 부산국제영화제 -> 부산국제영화제)
    name = re.sub(r'제\d+회\s*', '', name)
    # Remove "0000년"
    name = re.sub(r'\d{4}년', '', name)
    # Remove "20nn " (e.g., 2017 얼음나라화천 산천어축제 -> 얼음나라화천 산천어축제)
    name = re.sub(r'\d{4}\s*', '', name)
    # Remove leading/trailing whitespace
    name = name.strip()
    return name

# Apply the cleaning function to the '시설명' column of the most frequent festivals dataframe
ranked_top50_all_years['시설명_cleaned'] = ranked_top50_all_years['시설명'].apply(clean_festival_name)

# Extract the cleaned festival names
cleaned_fes_df = ranked_top50_all_years['시설명_cleaned']

# Perform word analysis on the cleaned names
# okt = konlpy.tag.Okt()
# cleaned_word_df = pd.DataFrame({'word': okt.nouns(' '.join(li for li in cleaned_fes_df.astype(str)))})

# Generate word count table for cleaned names
# Group by cleaned festival name and count the occurrences
cleaned_grouped_festival_counts = ranked_top50_all_years.groupby('시설명_cleaned').size().reset_index(name='빈도수')

# Sort by the count in descending order
cleaned_most_frequent_festivals = cleaned_grouped_festival_counts.sort_values(by='빈도수', ascending=False)

# cleaned_most_frequent_festivals.to_csv('/content/drive/MyDrive/WooriFISA/EDA/축제/축제_빈도수cleaned.csv', index=False)

# 상위 20개 축제의 빈도수를 시각화 (원하는 개수만큼 head() 조절)
fig = px.bar(cleaned_most_frequent_festivals.head(20),
             x='시설명_cleaned',
             y='빈도수',
             text='빈도수', # 막대에 빈도수 값 표시
             title='클리닝된 축제 이름별 빈도수 (상위 20개)')

fig.update_layout(xaxis_tickangle=-45) # x축 라벨 기울기 조절
st.markdown("<h3>🎡축제 검색량</h3>",unsafe_allow_html=True)

st.markdown(": 제 00회, 축제 앞 연도 제거한 축제")
st.plotly_chart(fig)

# 공식 지역명 리스트 (광역시, 시)
official_regions = ['서울','부산','대구','인천','광주','대전','울산','세종','수원','용인','고양','화성','성남','부천','남양주','안산','평택','안양','시흥','파주',
        '김포','의정부','광주','하남','양주','광명','군포','오산','이천','안성','구리','포천','의왕','양평','여주','동두천','과천','가평','연천',
        '춘천','원주','강릉','동해','태백','속초','삼척','홍천','영월','평창','정선','철원','화천','양구','인제','고성','양양',
        '청주','충주','제천','보은','옥천','영동','증평','진천','괴산','음성','단양',
        '천안','공주','보령','아산','서산','논산','계룡','당진','금산','부여','서천','청양','홍성','예산','태안',
        '전주','군산','익산','정읍','남원','김제','완주','진안','무주','장수','임실','순창','고창','부안',
        '목포','여수','순천','나주','광양','담양','곡성','구례','고흥','보성','화순','장흥','강진','해남','영암','무안','함평','영광','장성','완도','진도','신안',
        '포항','경주','김천','안동','구미','영주','영천','상주','문경','경산','의성','청송','영양','영덕','청도','고령','성주','칠곡','예천','봉화','울진','울릉',
        '창원','진주','통영','사천','김해','밀양','거제','양산','의령','함안','창녕','고성','남해','하동','산청','함양','거창','합천','제주','서귀포']

# 지역명이 어디에 포함되어 있든 제거하는 함수
def remove_region_anywhere(name):
    result = str(name)  # Ensure name is a string
    for region in official_regions:
        if region in result:
            result = result.replace(region, "")
    return result.strip()

# Apply the cleaning function to the '시설명_cleaned' column
cleaned_most_frequent_festivals['시설명_지역포함제거'] = cleaned_most_frequent_festivals['시설명_cleaned'].apply(remove_region_anywhere)

# Remove "축제" from the festival names after region removal
cleaned_most_frequent_festivals['시설명_지역및축제제거'] = cleaned_most_frequent_festivals['시설명_지역포함제거'].str.replace('축제', '', regex=False).str.strip()


# Group by the new column and sum the frequencies
festival_counts_no_region_or_chukje = cleaned_most_frequent_festivals.groupby('시설명_지역및축제제거')['빈도수'].sum().reset_index(name='빈도수_합계')

# Sort by the count in descending order
festival_counts_no_region_or_chukje = festival_counts_no_region_or_chukje.sort_values(by='빈도수_합계', ascending=False)



# 워드 클라우드 생성에 사용할 폰트 경로 설정
font_path = r'./data/BMDOHYEON_ttf.ttf'

dic_word = dict(zip(festival_counts_no_region_or_chukje['시설명_지역및축제제거'], festival_counts_no_region_or_chukje['빈도수_합계']))

# 워드 클라우드 객체 생성
wordcloud = WordCloud(font_path=font_path,
                      width=800,
                      height=800,
                      background_color='white',
                      max_words=100,
                      ).generate_from_frequencies(dic_word)

st.markdown("<h3>전국 축제에 대한 검색량</h3>", unsafe_allow_html=True)

# 워드 클라우드 시각화
# plt.figure(figsize=(10, 10))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# st.pyplot(plt)
st.image("./data/축제_워드클라우드.png", caption="워드클라우드 결과", use_container_width=True)

st.markdown('---')

st.markdown("<h3>축제 키워드</h3>", unsafe_allow_html=True)
st.dataframe(festival_counts_no_region_or_chukje.head(20), use_container_width=True)


st.markdown("""
<h3>🧩 관찰 포인트</h3> 
""", unsafe_allow_html=True)

st.markdown("""
백제문화제와 국제영화제가 가장 중심이 되는 키워드
            
지역 특산물 기반 축제 키워드 다수: 송어, 사과, 대추, 도자기
            
꽃 관련 봄축제 키워드 매우 빈번: 매화, 장미, 벚꽃, 코스모스
""")