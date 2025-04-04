import asyncio

from openai import OpenAI

from data.config import CHATGPT_API_KEY
from bot import dp

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
        await dp.bot.send_message(chat_id='523886206', text=f'openai error {e}')
        return f"openai error: {str(e)}"

# model="gpt-4o-mini",