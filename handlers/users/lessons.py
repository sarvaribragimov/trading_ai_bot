from loader import bot,dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.user import User
from aiogram import types

# @dp.callback_query_handler(lambda c: c.data, state=User.lessons_btn)
# async def poc_callback_but(call: types.CallbackQuery,  state: FSMContext):
#     print('dddddddddddddd')
#     user_data = await state.get_data()
#     lang = user_data['lang']

# Admin panel page

