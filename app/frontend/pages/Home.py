import streamlit as st

# st.write("내 질병/복용약 정보를 기반으로 약 복용 가능 여부를 확인해줍니다.")

col1, col2 = st.columns([1, 1])   

with col1:
    if st.button("내 정보 등록"):
        st.switch_page("pages/UserInfo.py")

with col2:
    if st.button("약 확인하기"):
        st.switch_page("pages/Chat.py")

st.image("C:\Potenup\Drug-Detection-Chatbot/app/frontend/resources/title.png", width='stretch')