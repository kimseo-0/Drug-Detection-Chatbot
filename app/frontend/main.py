# uv add openai python-dotenv streamlit
# uv add streamlit==1.49.1
# .env 파일 만들어서 OPENAI_API_KEY 추가해두기
# 서버 실행: streamlit run main.py
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
        title="챗봇",
        icon="🤖",
    )
]


st.title("💊 약물 복용 확인 챗봇")
nav = st.navigation(pages)
nav.run()