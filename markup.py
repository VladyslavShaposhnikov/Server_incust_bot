from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# main menu
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Привет!", "Добрый день!"]
keyboard.add(*buttons)

# cancel chat
def func(name):
    keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons2 = f"❌Выйти из чата {name}"
    keyboard2.add(buttons2)
    return keyboard2

# keyboard for client bot
def keyboard3(answ, show_iv):
    ky3 = InlineKeyboardMarkup()
    inline_kb3 = InlineKeyboardButton(text='Ответить', callback_data=answ)
    inline_kb31 = InlineKeyboardButton(text='Посмотреть событие', callback_data=show_iv)
    ky3.add(inline_kb3, inline_kb31)
    return ky3