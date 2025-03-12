import asyncio

from openai import OpenAI

from data.config import CHATGPT_API_KEY


async def openai(question):
    try:
        client = OpenAI(
          api_key=CHATGPT_API_KEY
        )
        response = client.chat.completions.create(
          model="gpt-4o-mini",
          store=True,
          messages=[
            {"role": "user", "content": question}
          ]
        )
        return str(response.choices[0].message.content)
    except Exception as e:
        return f"openai error: {str(e)}"

# -mini