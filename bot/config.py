from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from database import DataBase



TOKEN = '6318164318:AAGmx2ksOyS-fd8I5Etrl3e5TU-9S9yCP-M'

SELLERS_ID = [6896835332]
ADMIN_ID = 1

db = DataBase()

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)
