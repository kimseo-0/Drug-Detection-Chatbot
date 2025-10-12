from utils.api import get_user_profile

import streamlit as st 
pages = [
    st.Page(
        page="pages/Home.py",
        title="홈",
        icon="🏠",
        default=True
    ),
    st.Page(
        page="pages/UserInfo.py",
        title="정보입력",
        icon="👤",
    ),
    st.Page(
        page="pages/Chat.py",
        title="알약분석",
        icon="💊",
    )
]

TEST_USER_ID = "test2"  # 로컬 DB에서 불러올 기본 유저 ID

if "user_profile" not in st.session_state or not st.session_state["user_profile"]:
    try:
        test_profile = get_user_profile(TEST_USER_ID)
        if test_profile:
            st.session_state["user_id"] = TEST_USER_ID
            st.session_state["user_profile"] = test_profile
    except Exception as e:
        st.warning(f"❌ 프로필 자동 불러오기 실패")

st.title("💊 우리집 AI 약사", width="content")
nav = st.navigation(pages)
nav.run()