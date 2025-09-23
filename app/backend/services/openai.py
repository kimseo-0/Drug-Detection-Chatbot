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