from aiogram.dispatcher.filters.state import State, StatesGroup

class User(StatesGroup):
    lang = State()
    lessons = State()
    confirm = State()
    confirm_joined = State()

    menu = State()
    type = State()
    send_question = State()
    send_ticker = State()
    choose_question = State()
    premium = State()
    choose_tariff = State()



    payment = State()
    confirm_tariff = State()
    send_bill_check = State()




    admin = State()
    admin_channels = State()
    sendtousers = State()
    wait = State()
    signals = State()
    addsignal = State()
    addchannel = State()
    deletechannel = State()

    manage_tariff = State()
    addtariff = State()
    addtariffdays = State()
    addtariffprice = State()
    deletetariff = State()

    get_tokens = State()
    enter_tariff = State()
    enter_count = State()
    remove_user = State()
    barchart_token = State()
    enter_token = State()