from dotenv import load_dotenv 
load_dotenv()

from openai import OpenAI
client = OpenAI()

def chat(system_prompt, user):
    response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user
        }
    ],
    temperature = 0.7
    )

    answer = response.choices[0].message.content
    return answer

def chat5(system_prompt, user, verbosity = 'medium'):
    response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user
        }
    ],
    verbosity = verbosity # low: 간결, 핵심 위주, medium: 적당한 설명과 예시, high: 자세하고 풍부한 설명
    )

    answer = response.choices[0].message.content
    return answer