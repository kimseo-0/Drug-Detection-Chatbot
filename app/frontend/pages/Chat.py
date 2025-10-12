import streamlit as st
from utils.api import analyze_pill
import base64, os

TYPE_LABELS = {
    "pill": "알약 사진 (정제/캡슐)",
    "package": "포장지/설명서 (라벨/OCR)"
}

st.markdown("""
 <style>
    /* 기본 컨테이너 스타일 */
    .med-container {
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border-width: 3px;
        border-style: solid;
    }

    /* 섭취 가능 (Green) 스타일 */
    .usable {
        background-color: #e6ffe6;
        border-color: #00b300;
    }
    .usable .med-header {
        color: #008000;
    }

    /* 섭취 불가능 (Red) 스타일 */
    .unusable {
        background-color: #ffe6e6;
        border-color: #cc0000;
    }
    .unusable .med-header {
        color: #cc0000;
    }
    
    /* 공통 헤더 스타일 */
    .med-header {
        font-size: 1.5em; 
        margin-top: 0;
        margin-bottom: 5px;
    }

    /* 주의 성분 텍스트 스타일 */
    .caution-text, .unusable-reason-text {
        color: #cc0000;
        font-weight: bold;
        font-size: 1.1em;
        margin-top: -10px; /* 헤더와의 간격 줄임 */
        margin-bottom: 5px;
    }
    .unusable-reason-text {
        margin-top: 10px;
    }

    /* 이미지 및 텍스트 레이아웃 */
    .med-content-flex {
        display: flex; 
        align-items: flex-start; 
        margin-top: 15px;
    }
    .med-image {
        width: 100px; 
        height: 100px; 
        object-fit: contain; 
        margin-right: 15px; 
        border-radius: 5px;
    }
    .no-image-placeholder {
        border: 1px solid #ccc; 
        display: flex; 
        align-items: center; 
        justify-content: center;
    }
    
    /* 약품 상세 정보 텍스트 */
    .med-details h4 {
        margin: 0; 
        font-size: 1.3em;
    }
    .med-details p {
        margin: 5px 0 0 0; 
        font-size: 0.9em;
    }
    .med-details p:nth-child(2) { /* 효능과 주의/용법 사이 간격 줄임 */
            margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# 결과 표시
def display_medication_info(data, image_path="app/resources/zopistar_placeholder.png"):
    name = data.get("name", "정보 없음")
    effect = data.get("effect", "정보 없음")
    is_usable = data.get("isUsable", False)
    unusable_reason = data.get("unusable_reason", "")
    cautionary_ingredients = data.get("cautionary_ingredients", [])
    caution = data.get("caution", "정보 없음")

    # 배경색 및 테두리 색상 설정
    if is_usable:
        # 섭취 가능(green) 클래스 사용
        main_class = "usable" 
        header_text = "✅ 먹어도 됩니다!"
    else:
        # 섭취 불가능(red) 클래스 사용
        main_class = "unusable"
        header_text = "🚫 먹으면 안됩니다!"
    
    cautionary_ingredients_html = ""
    if cautionary_ingredients and not is_usable:
        cautionary_ingredients_html = f"<p class='caution-text'>{', '.join(cautionary_ingredients)} 성분 함유</p>"
    
    unusable_reason_html = ""
    if not is_usable and unusable_reason:
        unusable_reason_html = f"<p class='unusable-reason-text'>섭취 불가능 이유: {unusable_reason}</p>"

    def image_to_base64(image_path):
        if not os.path.exists(image_path):
            return None
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        # MIME 타입은 이미지 파일에 따라 달라질 수 있으나, 일반적으로 png/jpeg를 가정
        return f"data:image/png;base64,{encoded_string}"
        
    # 3. 이미지 Base64 인코딩
    base64_img = image_to_base64(image_path)
    img_html = ""
    if base64_img:
        img_html = f'<img src="{base64_img}" class="med-image">'
    else:
        img_html = f'<div class="med-image no-image-placeholder">No Image</div>'

    # 5. CSS 스타일 정의 및 단일 st.markdown 블록 구성
    full_markdown_content = f"""
    <div class="med-container {main_class}">
        <h3 class="med-header">{header_text}</h3>
        <h4>{name}</h4>
        <div>{cautionary_ingredients_html}</div>
        <img src="{base64_img}" class="med-image">
        <div class="med-details">
            <p><b>효능:</b> {effect}</p>
            <p><b>주의:</b> {caution}</p>
        </div>
        <div>{unusable_reason_html}</div>
    </div>
    """
    
    st.markdown(full_markdown_content, unsafe_allow_html=True)



# 세션에 저장된 유저 프로필 확인
user_profile = st.session_state.get("user_profile")
user_id = st.session_state.get("user_id")
if user_profile:
    # 홈으로 돌아가기 버튼
    if st.button("홈으로 이동"):
        st.switch_page("pages/Home.py")

    with st.expander(label="내 정보 요약"):
        st.markdown(
            f"""
            <div>
                <b>질병</b>: {', '.join(user_profile.get('disease', [])) or '없음'}<br>
                <b>주의 약품</b>: {', '.join(user_profile.get('caution_drugs', [])) or '없음'}<br>
                <b>주의 성분</b>: {', '.join(user_profile.get('caution_ingredients', [])) or '없음'}<br>
                <b>복용 중 약</b>: {', '.join(user_profile.get('current_medications', [])) or '없음'}<br>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
        
        if img_type == "package":
            drug_name = st.text_input("약품명을 입력하세요:")

    if st.button("분석하기", use_container_width=True):
        if not uploaded:
            st.warning("이미지를 먼저 업로드해주세요.")
            st.stop()

        # FastAPI 호출 (타입별 라우팅은 서버에서 처리)
        with st.spinner("분석 중..."):
            try:
                print(f'{user_id} 가 패키지 분석 요청함')
                if img_type == "pill":
                    res = analyze_pill(user_id, uploaded, image_type=img_type)
                elif img_type == "package":
                    res = analyze_pill(user_id, uploaded, image_type=img_type, drug_name = drug_name)
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
                    st.write("**알약 패키지 분석 결과**")
                    # st.json(res.get("ocr"))
                    display_medication_info(res.get("ocr")['result'], res.get("image_path"))

            except Exception as e:
                st.error(f"분석 실패: {e}")
else:
    st.warning("등록된 사용자 정보가 없습니다. 정보를 먼저 등록하세요.")
    if st.button("유저 등록하러 가기"):
        st.switch_page("pages/UserInfo.py")

# display_medication_info({
#   "name": "타이레놀",
#   "effect": "감기로인한발열및동통(통증),두통,신경통,근육통,월경통,염좌통(뻔통증),치통,관절통,류마티양동통(통증이상또는그병력)",
#   "isUsable": True,
#   "unusable_reason": "없음",
#   "cautionary_ingredients": [],
#   "caution": "이 약은 아세트아미노펜을 주성분으로 한 비마약성 진통제입니다. 간손상 위험이 있으니 일일 최대 용량(4,000mg)을 초과하지 않도록  하며, 간 질환이 있거나 술을 자주 마시는 분은 주의가 필요합니다. 피부  이상반응이나 과민반응 시 즉시 복용을 중단하고 의사와 상담하십시오."   
# }, "C:/Potenup/Drug-Detection-Chatbot/app/uploaded_images/20251010_232834_타이레놀_패키지.jpg")