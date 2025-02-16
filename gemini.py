from data import config
import re
from data.config import GOOGLE_API_KEY
import httpx
import asyncio
from bing import search_bing, google_search
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
headers = {
    'Content-Type': 'application/json',
}
def remove_urls(text):
    # Define a regular expression pattern for matching URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')

    # Use the sub() function to replace URLs with an empty string
    clean_text = re.sub(url_pattern, '', text)

    return clean_text
async def generate(text):
    params = {
        'key': GOOGLE_API_KEY,
    }
    print('gemini start')
    data = {'contents': [{'parts': [{'text': text}]}]}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers, params=params, timeout=20)
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result.keys():
                if 'content' in result['candidates'][0].keys():
                    return result['candidates'][0]['content']['parts']
    return []


# async def main():
#     result = await _generate("what do know about uzbekistan?")
#     print(result)
# asyncio.run(main())

async def openai_model(q):
    searched = await google_search(q)
    contents = ' '.join([f"{i['content']}\n\n" for i in searched])
    api_key = "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"
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    contents = f"Today's data: {contents}\n"
    text = f'Answer the question: "{q}", following this content: \n' + contents

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )
    print(response)
# asyncio.run(openai_model("What is the recent analysist predictions of the ‘AAPL’ stock?"))



async def _generate(text):
    searched = await google_search(text)
    contents = ' '.join([f"{i['content']}\n\n" for i in searched])#Title: {i['name']}\nURL: {i['url']}\nContent:
    text = f'"{text}"'
    print(contents)
    text = f'Answer the question: "{text}", following this information: \n' + contents
    print(text)
    result = await generate(text)
    print(result)
    return result
if __name__ == "__main__":
    asyncio.run(_generate("Top 10  the most active stocks in the U.S. stock market today?"))
    # asyncio.run(generate("what date is it in fergana/uzbekistan?"))
