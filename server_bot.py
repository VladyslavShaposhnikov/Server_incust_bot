from aiogram.utils import executor
from create_bot import dp
from handlers import server

async def start_bot(_):
    print('Bot is ready to work!!!')

server.register_hendlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=start_bot)