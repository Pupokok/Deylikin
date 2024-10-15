from aiogram.types import Message
from aiogram import types, F, Router
from aiogram.filters import CommandStart, CommandObject, Command

from dotenv import load_dotenv

from keyboards import kb_client_main


load_dotenv()
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! �� бот для управления вашими заявками. Выбери действие:", 
                         reply_markup=kb_client_main)