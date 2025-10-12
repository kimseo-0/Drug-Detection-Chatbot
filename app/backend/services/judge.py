import pandas as pd
from typing import Optional
from services import openai
from infra import db    
import json

def check_available_durg(user_id, data, user_text):
    profile = db.get_user_profile(user_id)
    user_data = ""
    user_data += ', '.join(profile.get('disease', [])) or '없음'
    user_data += ', '.join(profile.get('caution_drugs', [])) or '없음'
    user_data += ', '.join(profile.get('caution_ingredients', [])) or '없음'
    user_data += ', '.join(profile.get('current_medications', [])) or '없음'

    system_prompt = f"""
        당신은 약품 성분에 대해서 잘 알고 있는 약사 AI 입니다.
        [사용자 정보]를 통해 사용자가 가지고 있는 병과, 주의해야하는 알약, 주의해야하는 성분을 확인하고
        [사전 정보]와 비교하여 [입력정보]로 들어오는 약이 섭취 가능한지 판단해야합니다.

        [판단 방법]
        1단계: [사용자 정보]의 'caution_drugs'이 해당 약품이 포함되는 경우 섭취 불가능
        2단계: [사용자 정보]의 'caution_ingredients'이 약품의 [제품명] 또는 [성분/함량] 또는 [첨가물]에 포함되는 경우 섭취 불가능
        3단계: [사용자 정보]의 'disease'의 질병을 가지고 있는 경우 해당 약품의 [주의사항]에서 해당 질병이 있을 경우 주의해야한다는 설명이 있을 경우 섭취 불가능
        4단계: [사용자 정보]의 'current_medications'과의 상호작용 가능성이 있는지 확인, 부정적 상호작용이 있을 경우 섭취 불가능
        * 1-4 단계를 모두 통과할 경우 섭취 가능하다고 판단한다
        * 명확하게 섭취가 불가능한 경우가 아닌경우는 섭취 가능하다고 판단한다
        
        [사용자 정보]
        {user_data}

        [사용자 정보 설명]
        없음이라고 작성되었다면 해당 질병이 없거나, 주의한 성분이 없다는 뜻이므로 무시한다.
        disease: 사용자가 가지고 있는 질병 명들
        caution_drugs : 사용자가 주의해야하는 약품 명들 (주의해야하는 약품과 비슷한 성분이 있을 경우 미섭취 권장)
        caution_ingredients : 사용자가 섭취할 수 없는 주의해야하는 성분, 첨가물 등 (주의해야하는 성분이 있을 경우 미섭취 권장)
        current_medications : 사용자가 복용 중인 약
        
        [사전 정보]
        {data}
        
        [입력 정보]
        섭취하려는 약에 대한 이름

        [출력 형식]
        {{
            "name" : "제품명",
            "effect" : "이 약의 효능",
            "isUsable" : "섭취 가능 여부를 Bool 값으로",
            "unusable_reason" : "[사용자 정보]를 바탕으로 섭취가 불가능한 이유를 설명합니다, 섭취 가능한 경우 빈칸으로 제공합니다",
            "cautionary_ingredients" : "[사용자 정보]에서 섭취 불가능한 이유가 되는 주의 성분을 리스트로 제공합니다, 섭취 가능한 경우 빈칸으로 제공합니다",
            "caution" : "이 약품의 일반적인 주의사항을 제공합니다"
        }}
        """
    
    result = openai.chat(system_prompt, user_text)
    result = json.loads(result)
    return result

def check_available_drug_package(user_id, data, user_text):
    profile = db.get_user_profile(user_id)
    user_data = ""
    user_data += ', '.join(profile.disease) or '없음'
    user_data += ', '.join(profile.caution_drugs) or '없음'
    user_data += ', '.join(profile.caution_ingredients) or '없음'
    user_data += ', '.join(profile.current_medications) or '없음'
    print(user_data)

    system_prompt = f"""
        당신은 약품 성분에 대해서 잘 알고 있는 약사 AI 입니다.
        [사용자 정보]를 통해 사용자가 가지고 있는 병과, 주의해야하는 알약, 주의해야하는 성분을 확인하고
        [사전 정보]와 비교하여 [입력정보]로 들어오는 약이 섭취 가능한지 판단해야합니다.

        [판단 방법]
        1단계: [사용자 정보]의 'caution_drugs'이 해당 약품이 포함되는 경우 섭취 불가능
        2단계: [사용자 정보]의 'caution_ingredients'이 약품의 [제품명] 또는 [성분/함량] 또는 [첨가물]에 포함되는 경우 섭취 불가능
        3단계: [사용자 정보]의 'disease'의 질병을 가지고 있는 경우 해당 약품의 [주의사항]에서 해당 질병이 있을 경우 주의해야한다는 설명이 있을 경우 섭취 불가능
        4단계: [사용자 정보]의 'current_medications'과의 상호작용 가능성이 있는지 확인, 부정적 상호작용이 있을 경우 섭취 불가능
        * 1-4 단계를 모두 통과할 경우 섭취 가능하다고 판단한다
        
        [사용자 정보]
        {user_data}

        [사용자 정보 설명]
        없음이라고 작성되었다면 해당 질병이 없거나, 주의한 성분이 없다는 뜻이므로 무시한다.
        disease: 사용자가 가지고 있는 질병 명들
        caution_drugs : 사용자가 주의해야하는 약품 명들 (주의해야하는 약품과 비슷한 성분이 있을 경우 미섭취 권장)
        caution_ingredients : 사용자가 섭취할 수 없는 주의해야하는 성분, 첨가물 등 (주의해야하는 성분이 있을 경우 미섭취 권장)
        current_medications : 사용자가 복용 중인 약
        
        [사전 정보]
        {data}
        
        [입력 정보]
        섭취하려는 약에 대한 이름

        [출력 형식]
        {{
            "name" : "제품명",
            "effect" : "이 약의 효능",
            "isUsable" : "섭취 가능 여부를 Bool 값으로",
            "unusable_reason" : "[사용자 정보]를 바탕으로 섭취가 불가능한 이유를 설명합니다, 섭취 가능한 경우 빈칸으로 제공합니다",
            "cautionary_ingredients" : "[사용자 정보]에서 섭취 불가능한 이유가 되는 주의 성분을 리스트로 제공합니다, 섭취 가능한 경우 빈칸으로 제공합니다",
            "caution" : "이 약품의 일반적인 주의사항을 제공합니다"
        }}
        """
    
    result = openai.chat(system_prompt, user_text)
    result = json.loads(result)
    return result