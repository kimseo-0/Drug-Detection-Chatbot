import streamlit as st
import UserInfo
import Chat
from utils.api import get_user_profile

TEST_USER_ID = "test"  # 로컬 DB에서 불러올 기본 유저 ID

def run():
    # 기본 페이지 상태
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

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

    # 라우팅
    if st.session_state["page"] == "Home":
        st.title("내 알약 확인 서비스")
        # st.write("내 질병/복용약 정보를 기반으로 약 복용 가능 여부를 확인해줍니다.")
        st.image("C:\Potenup\Drug-Detection-Chatbot/app/frontend/resources/title.png", width='stretch')
        
        col1, col_space, col2 = st.columns([1, 1, 1])   

        with col1:
            if st.button("내 정보 등록하러 가기"):
                st.session_state["page"] = "UserInfo"

        with col2:
            if st.button("챗봇으로 확인하기"):
                st.session_state["page"] = "Chat"

    elif st.session_state["page"] == "UserInfo":
        UserInfo.run()

    elif st.session_state["page"] == "Chat":
        Chat.run()
    
if __name__ == "__main__":
    run()
