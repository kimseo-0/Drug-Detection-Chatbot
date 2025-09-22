import streamlit as st
from utils.api import get_user_profile

TEST_USER_ID = "test"  # 로컬 DB에서 불러올 기본 유저 ID

# 세션에 사용자 정보가 없으면 로컬 DB에서 'test' 유저 자동 로드 시도
if "user_profile" not in st.session_state or not st.session_state["user_profile"]:
    try:
        test_profile = get_user_profile(TEST_USER_ID)
        if test_profile:
            st.session_state["user_profile"] = test_profile
            st.session_state["page"] = "Chat"  # 바로 챗봇으로
    except Exception as e:
        st.warning(f"❌ 프로필 자동 불러오기 실패: {e}")
        pass

# st.write("내 질병/복용약 정보를 기반으로 약 복용 가능 여부를 확인해줍니다.")

col1, col2 = st.columns([1, 1])   

with col1:
    if st.button("내 정보 등록"):
        st.switch_page("pages/UserInfo.py")

with col2:
    if st.button("약 확인하기"):
        st.switch_page("pages/Chat.py")

st.image("C:\Potenup\Drug-Detection-Chatbot/app/frontend/resources/title.png", width='stretch')