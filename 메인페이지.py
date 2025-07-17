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
👩‍💻 **승보**:  
            
공공데이터포털에서 Open API를 호출하는데 계속 오류가 났어요!
<br>데이터별 참고 문서가 잘 나와있어서 해결했습니다!

<br>

🧑‍💻 **수빈**:  

북한에 다녀올 뻔 했어요ㅜ

<br>

🧑‍💻 **효림** :  
            
서울시 축제 참여 만족도 데이터를 전처리 할 때 이혼/별거 집단의 매우불만족 비율이 결측치였습니다.
<br>매우 만족 ~ 매우 불만족 다섯 개의 카테고리로 이루어져 있기 때문에 다른 선택지의 비율을 더해 100에서 빼는 방식으로 해당 결측치를 채울 수 있었어요!

<br>

🧑‍💻 **하연** :  

            
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("<p style='text-align:center;'>지방의 숨겨진 매력을 세상에 알리는 프로젝트 🌿Go지방🌿에 오신 걸 환영합니다!</p>", unsafe_allow_html=True)
