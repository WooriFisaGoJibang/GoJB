import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Go지방", layout="wide")

# ------------------------
# 헤더 영역
# ------------------------
st.markdown("<h1 style='text-align: center;'>Welcome Go지방🚀</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>지방에 살기 어렵다면, 놀러는 오게 만들자!</h4>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------
# 1. 서비스 소개
# ------------------------
st.subheader("📌 서비스 소개")

st.markdown("""
**Go지방**은 사람들이 잘 모르는 지역의 축제, 문화 자산, 관광 자원을 발굴하고 소개하는 플랫폼입니다.  
**왜 지방으로 놀러 가야 할까**라는 질문에 답하며, 새로운 여행 목적지를 제안합니다.

**주요 기능**
- 💡 근대 건축물, 문화유산, 숨은 축제 정보 소개
- 📊 지방 축제/관광 키워드 검색량 분석
""")

st.markdown("<br><br>", unsafe_allow_html=True)

# ------------------------
# 2. 제작 배경
# ------------------------
st.subheader("🛠 제작 배경")

st.markdown("""
모든 팀원이 **지방 출신**으로서, 지방 소멸과 지역 경제 침체에 대해 깊이 고민하게 되었습니다.  
수도권에 몰린 문화생활과 해외여행 쏠림 현상 속에서, **어떻게 하면 지방 방문률을 높일 수 있을까**를 주제로 프로젝트를 시작했습니다.
            
서울에는 다양한 문화생활이 존재하고 이에 따라 자연스럽게 참여율 또한 높다는 생각이 들었습니다.  
**서울 축제**와 관련된 통계 조사 자료를 살펴보며 어떤 집단의 축제 참여율이 높은지 살펴보았습니다.
            
대부분의 사람들이 지역별로 어떤 축제가 있는지 잘 모르는 경우가 많고, 홍보가 잘 되지 않은 **숨어있는 다양한 축제**들이 많다는 생각이 들었습니다.
     

<br>
            
           
> 근대 건축물 데이터는 매우 부족했고, 지자체별 관리가 미흡했습니다.<br>
> 지역 축제의 경우 많은 사람이 “어디서 무엇이 열리는지”조차 모르는 경우가 많았습니다.

<br>
            
**💡 새로운 관광 자원 개발**            
숨어있는 근대 건축물과 문화유산, 지역 축제를 발굴하여 관광 콘텐츠로 재해석

**📈 데이터로 격차 줄이기**            
수도권과 비수도권 간의 문화/관광 격차 해소를 목표로, 데이터를 통해 지역 활성화 가능성을 진단

""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ------------------------
# 3. 팀원 소개
# ------------------------
st.subheader("👩‍💻 팀원 소개")

cols = st.columns(4)

with cols[0]:
    st.markdown("**하승보🍜**")
    st.markdown("- 문화유산 map 작성")
    st.markdown("- 주제 선정")

with cols[1]:
    st.markdown("**최수빈🍖**")
    st.markdown("- 지역축제 map 작성")
    st.markdown("- 방문객 수 / 지역축제 수 분석")

with cols[2]:
    st.markdown("**조효림🥔**")
    st.markdown("- 서울축제 시각화")
    st.markdown("- 소개 streamlit 작성")

with cols[3]:
    st.markdown("**최하연🍞**")
    st.markdown("- 축제 키워드 분석")
    st.markdown("- 데이터 수집 및 전처리")

st.markdown("<br><br>", unsafe_allow_html=True)
# ------------------------
# 4. 트러블슈팅
# ------------------------
st.subheader("☄️ 트러블슈팅")

st.markdown("""
👩‍💻 **승보**  
&nbsp;&nbsp;1. **공공데이터포털 API 읽기**  
&nbsp;&nbsp;&nbsp;&nbsp;- 원인 분석: 방법을 몰라서 시도하지 못함  
&nbsp;&nbsp;&nbsp;&nbsp;- 해결 방안: 상세페이지를 참고함  

&nbsp;&nbsp;2. **folium으로 지도 만들기**  
&nbsp;&nbsp;&nbsp;&nbsp;- 데이터마다 label이 달라서 맞춰야 했음  
&nbsp;&nbsp;&nbsp;&nbsp;- 해당 지역에 0개면 까만 색으로 나타나서, 색상 변경 원함  
&nbsp;&nbsp;&nbsp;&nbsp;- 해결 방안: folium 공식 문서 참고  

<br>

🧑‍💻 **수빈**  

&nbsp;&nbsp;1. **잘못된 축제 위치 데이터 처리**  
&nbsp;&nbsp;&nbsp;&nbsp;- 경기도 안산시에서 개최된 축제 중 하나가 북한에 표시됨  
&nbsp;&nbsp;&nbsp;&nbsp;- 원인 분석:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 축제 데이터의 위도가 실제(37.310742)가 아니라 오타로 38.310742로 잘못 입력됨  
&nbsp;&nbsp;&nbsp;&nbsp;- 해결 방법:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 대한민국 시군구 경계 데이터를 기준으로  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 올바른 행정구역 내에 포함되는지 확인  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 행정구역 기반 좌표 재검증/정제 로직 적용

&nbsp;&nbsp;2. **대용량 파일 Git 업로드 문제**  
&nbsp;&nbsp;&nbsp;&nbsp;- 용량이 큰 데이터 파일이 Git에 업로드되지 않는 문제  
&nbsp;&nbsp;&nbsp;&nbsp;- 원인 분석:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Git의 기본 용량 제한 500MB  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 단일 파일 최대 100MB 제한  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 일반 커밋 방식으로는 업로드 불가  
&nbsp;&nbsp;&nbsp;&nbsp;- 해결 방법:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Git LFS(Large File Storage) 설치  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 해당 파일 형식을 LFS로 tracking  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• .gitattributes 파일로 유형별 LFS tracking 지정 후 업로드

<br>

🧑‍💻 **효림**  
&nbsp;&nbsp;1. **서울 축제 데이터의 표본 수 미포함 문제**  
&nbsp;&nbsp;&nbsp;&nbsp;- 20대, 남성/여성 등 범주 비율만 있고,  
&nbsp;&nbsp;&nbsp;&nbsp;  20대 여성과 같은 세부 집단 정보는 없음  

&nbsp;&nbsp;2. **결측치 처리**  
&nbsp;&nbsp;&nbsp;&nbsp;- 서울시 축제 만족도 데이터에서  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 이혼/별거 집단의 “매우불만족” 비율이 결측  
&nbsp;&nbsp;&nbsp;&nbsp;- 해결 방법:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 매우 만족~매우 불만족 5개 카테고리의 합이 100이 되도록,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 나머지 4개 카테고리 비율을 더해 100에서 빼는 방식으로 Impute

<br>

🧑‍💻 **하연**  

&nbsp;&nbsp;1. **워드클라우드 축제 키워드 추출 이슈**  
&nbsp;&nbsp;&nbsp;&nbsp;- 축제명에서 지역명·키워드 분리를 어떻게 할지 고민  
&nbsp;&nbsp;&nbsp;&nbsp;- 원인 분석:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 축제명에 지역명이 포함되어 있어 키워드가 혼재  
&nbsp;&nbsp;&nbsp;&nbsp;- 해결 방법:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 공공데이터포털에서 전국 ‘시’ 단위 지역명 데이터 수집  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 정렬된 지역명 리스트 추출  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 축제명에서 해당 지역명 제거해서  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 순수 키워드만 남도록 전처리 로직 구현

""", unsafe_allow_html=True)


st.markdown("---")

st.markdown("<p style='text-align:center;'>지방의 숨겨진 매력을 세상에 알리는 프로젝트 🌿Go지방🌿에 오신 걸 환영합니다!</p>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<br>
<b>데이터 출처</b><br>
<br>
- 공공데이터포털 &gt; 서울특별시 축제 참여율 및 만족도 통계  
  <a href='https://www.data.go.kr/data/15085152/fileData.do' target='_blank'>https://www.data.go.kr/data/15085152/fileData.do</a>
<br>
- 디지털트윈국토 &gt; 행정구역시군구_경계  
  <a href='https://www.vworld.kr/dtmk/dtmk_ntads_s002.do?svcCde=MK&dsId=30604' target='_blank'>https://www.vworld.kr/dtmk/dtmk_ntads_s002.do?svcCde=MK&dsId=30604</a>
<br>
- 공공데이터포털 &gt; 전국문화축제표준데이터
  <a href='https://www.data.go.kr/data/15013104/standard.do' target='_blank'>https://www.data.go.kr/data/15013104/standard.do</a>
<br>
- 문화 빅데이터 플랫폼 &gt; 전국 축제 트렌드 지도  
  <a href='https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=bdd518d0-e65a-4621-9f34-23bace896ae5' target='_blank'>https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=bdd518d0-e65a-4621-9f34-23bace896ae5</a>
<br>            
- 한국 관광 데이터랩 &gt; 광역시별 외지인 방문자수  
  <a href='https://datalab.visitkorea.or.kr/datalab/portal/bda/getMetcoAna.do#' target='_blank'>https://datalab.visitkorea.or.kr/datalab/portal/bda/getMetcoAna.do#</a>
""", unsafe_allow_html=True)

