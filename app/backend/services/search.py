import pandas as pd
from typing import Optional
from services import openai
import ast, json

_df: Optional[pd.DataFrame] = None

def load_data():
    global _df
    if _df is None:
        _df = pd.read_csv("C:\Potenup\Drug-Detection-Chatbot\data\\total_result_drug.csv")
    return _df

def search_drug_detail(user_text):
    if user_text == "없음":
        return []
    
    df = load_data()
    lines = [f"({i}, {name})" for i, name in df['제품명'].astype(str).items()]
    data = "\n".join(lines)

    system_prompt = f"""
    당신은 약 정보에 대한 CSV 데이터를 가지고 해당 데이터에서 검색을 하는 AI 입니다.
    알약에 대해서 키워드 검색을 하면 해당 알약과 관련된 모든 알약의 index 값을 찾는 것이 목표입니다.
    제품명에 해당 키워드를 포함하거나, 비슷한 경우 모두 index를 포함합니다.
    
    [사용자 입력]
    알약에 대한 키워드

    [사전 정보]
    {data}

    [출력 형식]
    해당 제품명에 해당하는 제품 인덱스 리스트 ex) [0, 1, 2, 3, 4, 5, 6], [0, 1, 2]
    """
    
    res = openai.chat(system_prompt, user_text)
    indexes = ast.literal_eval(res)

    result = []
    for index in indexes:
        row_str = json.dumps(df.iloc[int(index)].to_dict(), ensure_ascii=False)
        result.append(row_str)
    return result
