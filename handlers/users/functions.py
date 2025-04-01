from utils.db_api.database import DataBaseSql
from string import ascii_letters
from random import choices

async def list_tokens():
    db = DataBaseSql()
    tokens = await db.search(all=True)
    txt = f"<b>Umumiy tokenlar soni: {len(tokens)} ta</b>\n"
    count = 1
    for token in tokens:
        txt += f"{count}. <code>{token[0]}</code> \n"
        count += 1
    return txt

async def generate_token():
    letters = ascii_letters + "1234567890"
    token = "".join(choices(letters, k=9))
    while await DataBaseSql().search(token=token):
        token = "".join(choices(letters, k=9))
    return token