import streamlit as st
from utils.api import save_user_profile

def run():
    st.title("내 정보 등록")

    # user_id = st.text_input("사용자 ID")
    disease = st.text_input("질병")
    caution_drugs = st.text_area("주의 약품 (콤마로 구분)", placeholder="예: 아스피린, 와파린")
    caution_ingredients = st.text_area("주의 성분 (콤마로 구분)", placeholder="예: 카페인, 나트륨")
    current_medications = st.text_area("복용 중인 약 (콤마로 구분)", placeholder="예: 로사르탄, 아토르바스타틴")

    if st.button("저장 후 챗봇으로 이동"):
        profile = {
            "user_id": 'test',
            "disease": disease,
            "caution_drugs": [d.strip() for d in caution_drugs.split(",") if d.strip()],
            "caution_ingredients": [i.strip() for i in caution_ingredients.split(",") if i.strip()],
            "current_medications": [m.strip() for m in current_medications.split(",") if m.strip()],
        }

        try:
            result = save_user_profile(profile)
            st.success("✅ 사용자 정보가 저장되었습니다")

            # 저장된 유저 정보를 세션에 보관 (챗봇에서 활용 가능)
            st.session_state["user_profile"] = result
            st.session_state["page"] = "Chat"   # 바로 Chat 페이지로 이동

        except Exception as e:
            st.error(f"저장 실패: {e}")
