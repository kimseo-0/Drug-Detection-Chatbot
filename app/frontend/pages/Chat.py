import streamlit as st
from utils.api import analyze_pill
import base64

TYPE_LABELS = {
    "pill": "알약 사진 (정제/캡슐)",
    "package": "포장지/설명서 (라벨/OCR)"
}


# 세션에 저장된 유저 프로필 확인
user_profile = st.session_state.get("user_profile")
if user_profile:
    # 홈으로 돌아가기 버튼
    if st.button("홈으로 이동"):
        st.switch_page("pages/Home.py")

    with st.expander(label="내 정보 요약"):
        st.markdown(
            f"""
            <div>
                <b>질병</b>: {user_profile.get('disease') or '없음'}<br>
                <b>주의 약품</b>: {', '.join(user_profile.get('caution_drugs', [])) or '없음'}<br>
                <b>주의 성분</b>: {', '.join(user_profile.get('caution_ingredients', [])) or '없음'}<br>
                <b>복용 중 약</b>: {', '.join(user_profile.get('current_medications', [])) or '없음'},
            </div>
            """,
            unsafe_allow_html=True,
        )
    # st.write(f"**사용자 ID**: {user_profile.get('user_id')}")
    # st.write(f"**질병**: {user_profile.get('disease') or '없음'}")
    # st.write(f"**주의 약품**: {', '.join(user_profile.get('caution_drugs', [])) or '없음'}")
    # st.write(f"**주의 성분**: {', '.join(user_profile.get('caution_ingredients', [])) or '없음'}")
    # st.write(f"**복용 중 약**: {', '.join(user_profile.get('current_medications', [])) or '없음'}")
    
    with st.expander(label="어떤 이미지를 올릴까요?"):
        # st.subheader("어떤 이미지를 올릴까요?")
        img_type = st.radio(
            "이미지 종류 선택",
            options=["pill", "package"],
            format_func=lambda k: TYPE_LABELS[k],
            horizontal=True
        )

        uploaded = st.file_uploader("이미지 업로드 (jpg/png/jpeg)", type=["jpg", "jpeg", "png"])
        if uploaded:
            st.image(image=uploaded)

    if st.button("분석하기", use_container_width=True):
        if not uploaded:
            st.warning("이미지를 먼저 업로드해주세요.")
            st.stop()

        # FastAPI 호출 (타입별 라우팅은 서버에서 처리)
        with st.spinner("분석 중..."):
            try:
                res = analyze_pill(uploaded, image_type=img_type)
                st.success("분석 완료!")

                # 타입별 결과 표시 예시
                if res.get("mode") == "pill":
                    st.write("**분류 결과(알약 사진)**")
                    st.json(res.get("classification"))

                    if res.get("classification"):
                        r = res.get("classification")

                        for image_b64 in r['images']:
                            image = base64.b64decode(image_b64)
                            st.image(image, caption=r['label'], width="stretch")
                elif res.get("mode") == "package":
                    st.write("**OCR 결과(포장지/설명서)**")
                    # st.json(res.get("ocr"))

            except Exception as e:
                st.error(f"분석 실패: {e}")

else:
    st.warning("등록된 사용자 정보가 없습니다. 정보를 먼저 등록하세요.")
    if st.button("유저 등록하러 가기"):
        st.switch_page("pages/UserInfo.py")