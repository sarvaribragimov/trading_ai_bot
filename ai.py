import requests
import json
from data.config import MISTRAL_API_KEY

def send_api_request(content):
    url = 'https://api.mistral.ai/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {MISTRAL_API_KEY}',
        'Cookie': '__cf_bm=eug9j01ZRaTCHlZINoZN2u1UYVrOZ.5tDhV17jYPszo-1739794883-1.0.1.1-sKS12e6jdybhJZfZ29EkNORvC0Da_0xkCFBsGkimAIWWQZGBXF0ZISkFycpz.X9pBsDpQH4BPYbO0O0nMzMv2A'
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": content}]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Funksiyani chaqirish
result = send_api_request("Quyidagi 5ta savol shablonini eslab qol, va aksiya tikeri jonatganimda  sen mana shu shablon asosida javob bergin. "
                          "Savollarga aniq va qisqa javob bergin, javoblardagi umumiy belgilar soni 600tadan oshmasin. "
                          "1. “AAPL ticker” kompaniya biznes faoliyati "
                          "2. Bu hafta uchun “AAPL Tiker” aksiyasi uchun put /call ratio qiymatini va qancha put va qancha call option borligini aniqla "
                          "3. “AAPL ticker” aksiyasi uchun bugungi holat boyicha aksiyaning qancha foiz qismi Short-Sale qilinganligini aniqla "
                          "4. “AAPL ticker” aksiyaga oid oxirgi 3 kun Ichida qandaydir xabar chiqdimi, xabar sarlavhasini korsat va ijobiy yoki salbiy xabar ekanligni aniqlab qisqa javob ber "
                          "5. Yuqoridagi malumotlarga tayangan holda qisqa xulosangni ayt, ushbu kompaniya aksiyasini day trading uchun xarid qilsam boladimi yoki yoq?")
print(result)



