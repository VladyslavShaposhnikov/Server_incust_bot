from aiogram.dispatcher.dispatcher import Dispatcher    
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from create_bot import bot
from config import CLIENT_BOT_TOKEN
from markup import keyboard, func, keyboard3


# FSM class to send message in client bot
class Answer(StatesGroup):
    answer_text = State()


#@dp.message_handler(commands=['start', 'help'])
# start command
async def commands_start(message : types.message, state=FSMContext):
    await message.answer('Добро пожаловать {}!'.format(message.from_user.full_name), reply_markup=keyboard)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()

# @dp.callback_query_handler(text_contains='Ответить')
# inline button [Ответить]
async def answer(call: CallbackQuery, state:FSMContext):
    callback_list = call.data.split(',')
    ivent_name = callback_list[3]
    full_name = callback_list[1]
    chat_id = callback_list[2]
    ivent_id = callback_list[4]
    await call.message.answer(f'Вы вошли в час с {full_name}', reply_markup=func(full_name))
    await Answer.answer_text.set()
    async with state.proxy() as data:
        data['ivent_name'] = ivent_name
        data['chat_id'] = chat_id
        data['ivent_id'] = ivent_id

#@dp.message_handler(state=Answer.answer_text)
# send message to client
async def answer_txt(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['answer'] = message.text
        with bot.with_token(CLIENT_BOT_TOKEN):
            await bot.send_message(data['chat_id'], f'Сообщение от владельца события {data["ivent_name"]}\n{data["answer"]}', reply_markup=keyboard3(answ='chat'+str(data['ivent_id']), show_iv='id'+str(data['ivent_id'])))
    await answer()
    await state.finish()

# @dp.message_handler(lambda message: message.text.startswith("❌Выйти из чата"), state='*')
# cancel chat
async def cancel_chat(message:types.Message,state:FSMContext):
    current_state = await state.get_state()
    await message.answer('Вы вышли из чата', reply_markup=keyboard)
    if current_state is None:
        return
    await state.finish()

# @dp.callback_query_handler(text_contains='Посмотреть событие')
# inline button [Посмотреть событие] with deeplink
async def show_ivent(call: CallbackQuery):
    callback_list = call.data.split(',')
    id = callback_list[2]
    await call.message.answer(f'Нажмите на ссылку ниже что бы посмотреть событие\nhttps://t.me/Client_incust_bot?start={id}')


def register_hendlers(dp: Dispatcher):
    dp.register_message_handler(commands_start, lambda message: message.text == "/start", state='*', commands=['start', 'help'])
    dp.register_message_handler(cancel_chat, lambda message: message.text.startswith("❌Выйти из чата"), state='*')
    dp.register_callback_query_handler(answer, text_contains='Ответить')
    dp.register_message_handler(answer_txt, state=Answer.answer_text)
    dp.register_callback_query_handler(show_ivent, text_contains='Посмотреть событие')