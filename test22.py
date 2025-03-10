import asyncio

from beatifulsoup import get_column_inner_data
from data.utils import options_expirations, long_put_volume, long_put_volume_text, long_call_volume, \
    long_call_volume_text, put_call_ratios_text, getbarcharttableinfo
from utils.db_api import database


def alltext(ticker,comp_info,market_value,market_task,insider,invest):
    text = (f"Quyidagi malumotlarni o`rganib chiq va “stock tiker”   kompaniyasi uchun ijobiy yoki salbiy xabar ekanligini aniqla va javobing 800 ta belgidan oshmasin"
            f"kompaniya malumotlari: {market_value} {market_task}\n\n"
            f"“Stock tiker”  kompaniyasining so'ngi yangiliklari:{comp_info}   \n\n"
            f"Insayderlar savdosi:   {insider}\n\n "
            f"Instutsional transaction: {invest}")

    return text


async def getapi(ticker):
    col = await get_column_inner_data(ticker)
    col if isinstance(col, str) else str(col)
    print('coolll',col)


# async def test(ticker):
#     # te = await getapi(ticker)
#
#     barchart = await getbarcharttableinfo(ticker)
#     print(barchart)


asyncio.run(getapi('NVDA'))

