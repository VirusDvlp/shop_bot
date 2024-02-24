from asyncio import run

from config import bot, dp, db
from handlers import register_all_handlers


async def on_startup():
    register_all_handlers(dp)



async def on_shutdown():
    db.close()



async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    print('Бот начал работу')
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
