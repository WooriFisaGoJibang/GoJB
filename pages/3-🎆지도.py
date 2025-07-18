import streamlit as st
import pandas as pd
import folium
import json
import os
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Point
import re

st.set_page_config(layout="wide")
st.title("🎆 전국 근대문화유산 + 지역 문화축제 지도")

@st.cache_data
def load_data():
    try:
        df_heritage = pd.read_csv("data/KF_AREA_CLTUR_MDRN_CLTUR_HRITG_DATA_LIST_202312.csv", encoding='utf-8')
    except UnicodeDecodeError:
        df_heritage = pd.read_csv("data/KF_AREA_CLTUR_MDRN_CLTUR_HRITG_DATA_LIST_202312.csv", encoding='cp949')
    df_heritage = df_heritage.dropna(subset=['CTPRVN_NM', 'CTLSTT_LA', 'CTLSTT_LO'])
    df_heritage = df_heritage.drop_duplicates(subset=['CTLSTT_LA', 'CTLSTT_LO'], keep='first')
    heritage_count = df_heritage.groupby('CTPRVN_NM')['DATA_MANAGE_NO'].count()

    try:
        df_festival = pd.read_csv('data/전국문화축제표준데이터.csv', encoding='utf-8')
    except UnicodeDecodeError:
        df_festival = pd.read_csv('data/전국문화축제표준데이터.csv', encoding='cp949')
    df_festival = df_festival.dropna(subset=['위도', '경도'])
    df_festival = df_festival[df_festival['위도'] != 0]

    def extract_province(address):
        if pd.isna(address):
            return None
        return str(address).split()[0]
    df_festival['시도명'] = df_festival['소재지도로명주소'].apply(extract_province)
    df_festival['축제시작월'] = pd.to_datetime(df_festival['축제시작일자'], errors='coerce').dt.month
    df_festival['축제종료월'] = pd.to_datetime(df_festival['축제종료일자'], errors='coerce').dt.month

    # ▼▼▼ 축제명 정제 및 유사 축제명 그룹핑(회차, 연도 등 제거) ▼▼▼
    def clean_festival_title(title):
        """
        정규표현식으로 숫자/회차/연도 등 삭제 + 띄어쓰기 정리 + 대표명 반환
        ex) '2025년 제5회 상록수축제' -> '상록수축제'
        """
        s = str(title)
        # '제 n회', 'n회', 'YYYY년', 'YYYY' 등 제거
        s = re.sub(r'제\s*\d+\s*회', '', s)
        s = re.sub(r'\d+\s*회', '', s)
        s = re.sub(r'\d{4}년', '', s)
        s = re.sub(r'\d{4}', '', s)
        s = re.sub(r'\s+', '', s)  # 공백도 모두 제거 (연속 5자 일치 match 용이)
        return s.strip()

    # '정제된 축제명' 컬럼 추가
    df_festival['축제명_정제'] = df_festival['축제명'].apply(clean_festival_title)
    df_festival['축제시작일자'] = pd.to_datetime(df_festival['축제시작일자'], errors='coerce')

    # ▼▼▼ "연속 5글자 이상 일치"로 그룹핑/최신만 남김 ▼▼▼
    # 모든 '정제된 축제명' 간 비교, LCS(최장 공통 부분문자열) 5글자 이상이면 대표그룹 할당
    festival_names = df_festival['축제명_정제'].tolist()
    group_ids = [-1] * len(festival_names)
    group_counter = 0

    def lcs5(s1, s2):
        # 두 문자열에서 5글자 이상 연속으로 일치하는 부분이 있으면 True
        m = [[0]*(1+len(s2)) for _ in range(1+len(s1))]
        longest = 0
        for x in range(1,1+len(s1)):
            for y in range(1,1+len(s2)):
                if s1[x-1] == s2[y-1]:
                    m[x][y] = m[x-1][y-1] + 1
                    if m[x][y] > longest:
                        longest = m[x][y]
                else:
                    m[x][y] = 0
        return longest >= 5

    for i in range(len(festival_names)):
        if group_ids[i] != -1:
            continue
        group_ids[i] = group_counter
        for j in range(i+1, len(festival_names)):
            if group_ids[j] == -1 and lcs5(festival_names[i], festival_names[j]):
                group_ids[j] = group_counter
        group_counter += 1

    df_festival['축제그룹ID'] = group_ids

    # 그룹별 최신 하나만 남기기
    df_festival = df_festival.sort_values('축제시작일자', ascending=False)
    df_festival = df_festival.drop_duplicates(subset=['축제그룹ID'])

    festival_count = df_festival.groupby('시도명')['축제명'].count()
    all_regions = heritage_count.index.union(festival_count.index)
    heritage_count_full = heritage_count.reindex(all_regions).fillna(0)
    festival_count_full = festival_count.reindex(all_regions).fillna(0)
    combined_count = heritage_count_full + festival_count_full

    return df_heritage, df_festival, heritage_count_full, festival_count_full, combined_count

# == 이하 기존 코드 동일 ==
@st.cache_resource
def load_korea_boundary():
    gdf = gpd.read_file('data/N3A_G0100000.shp', encoding='cp949')
    if gdf.crs is not None and gdf.crs.to_string() != 'EPSG:4326':
        gdf = gdf.to_crs(epsg=4326)
    return gdf

월_라벨 = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
with st.sidebar:
    selected_months_label = st.multiselect("월별 지역문화축제 보기", 월_라벨, default=월_라벨)
    label_to_month = {l: i+1 for i, l in enumerate(월_라벨)}
    selected_months = [label_to_month[m] for m in selected_months_label]

def is_in_korea(lat, lon, gdf):
    point = Point(lon, lat)
    row = gdf[gdf.contains(point)]
    if not row.empty:
        return True, row['NAME'].values[0]
    else:
        return False, None

def filter_festival_within_korea(df_festival, gdf_korea):
    results = []
    for idx, row in df_festival.iterrows():
        lat, lon = row['위도'], row['경도']
        in_korea, region = is_in_korea(lat, lon, gdf_korea)
        results.append(in_korea)
    return df_festival.loc[results].reset_index(drop=True)

def create_map(show_heritage, show_festival, selected_months, gdf_korea):
    df_heritage, df_festival, heritage_count_full, festival_count_full, combined_count = load_data()
    map_osm = folium.Map(location=[36.5, 127.8], zoom_start=7)
    district_path = './data/korea.json'
    if os.path.exists(district_path):
        with open(district_path, encoding='utf-8') as f:
            district = json.load(f)
        if show_heritage and show_festival:
            color_data = combined_count
            legend_name = "근대문화유산+축제 개수 (지역별)"
        elif show_heritage:
            color_data = heritage_count_full
            legend_name = "근대문화유산 개수 (지역별)"
        elif show_festival:
            color_data = festival_count_full
            legend_name = "지역 문화축제 개수 (지역별)"
        else:
            color_data = None
        if color_data is not None:
            folium.Choropleth(
                geo_data=district,
                data=color_data,
                columns=[color_data.index, color_data.values],
                key_on="feature.properties.CTP_KOR_NM",
                fill_color="YlGn",
                fill_opacity=0.6,
                line_opacity=0.7,
                nan_fill_color='lightgray',
                legend_name=legend_name
            ).add_to(map_osm)
    if show_heritage:
        heritage_cluster = MarkerCluster(name="⚒ 근대문화유산").add_to(map_osm)
        for idx, row in df_heritage.iterrows():
            folium.Marker(
                location=[row["CTLSTT_LA"], row["CTLSTT_LO"]],
                popup=folium.Popup(row.get('DATA_TITLE_NM', 'NO TITLE'), max_width=300),
                icon=folium.Icon(color="orange", icon="university", prefix="fa")
            ).add_to(heritage_cluster)
    if show_festival:
        df_festival_month = df_festival[
            df_festival['축제시작월'].isin(selected_months) |
            df_festival['축제종료월'].isin(selected_months)
        ]
        df_festival_in_korea = filter_festival_within_korea(df_festival_month, gdf_korea)
        festival_cluster = MarkerCluster(name="🎉 지역 문화축제").add_to(map_osm)
        for idx, row in df_festival_in_korea.iterrows():
            festival_name = row['축제명']
            dates = f"{row['축제시작일자']} ~ {row['축제종료일자']}"
            location = row.get('소재지도로명주소', '')
            phone = row.get('전화번호', '')
            homepage = row.get('홈페이지주소', '')
            popup_html = f"""
            <b>{festival_name}</b><br>
            📅 {dates}<br>
            📍 {location}<br>
            ☎️ {phone}<br>
            🌐 <a href="{homepage}" target="_blank">홈페이지</a>
            """
            folium.Marker(
                location=[row['위도'], row['경도']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='purple', icon='star', prefix='fa')
            ).add_to(festival_cluster)
    folium.LayerControl().add_to(map_osm)
    return map_osm

show_heritage = st.checkbox("근대문화유산 보기", value=True, key="show_heritage_chkbx")
show_festival = st.checkbox("지역 문화축제 보기", value=True, key="show_festival_chkbx")
gdf_korea = load_korea_boundary()

# 월별 축제 목록 - 대한민국 영토 내 축제만 추출 (최신/정제 그룹 적용됨)
df_heritage, df_festival, heritage_count_full, festival_count_full, combined_count = load_data()
df_festival_month = df_festival[
    df_festival['축제시작월'].isin(selected_months) |
    df_festival['축제종료월'].isin(selected_months)
]
df_festival_in_korea = filter_festival_within_korea(df_festival_month, gdf_korea)
festival_display_cols = [
    '축제명', '축제시작일자', '축제종료일자', '소재지도로명주소', '홈페이지주소'
]
festival_table = df_festival_in_korea[festival_display_cols].reset_index(drop=True)

map_osm = create_map(show_heritage, show_festival, selected_months, gdf_korea)
st_folium(map_osm, width=900, height=650)
st.markdown('<div style="margin-bottom: -32px"></div>', unsafe_allow_html=True)
st.subheader("🎉 선택 월 축제 목록 (대한민국 영토 내 축제만, 중복·회차 통합 최신만)")
st.dataframe(festival_table, use_container_width=True)
