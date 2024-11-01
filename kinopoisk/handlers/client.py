import sys

from aiogram.types import Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command


from dotenv import load_dotenv

from keyboards.kb_client import kb_client_main, kb_log_in
from utils.states import LogState
from kin import selen


load_dotenv()
router = Router()

@router.message(Command('stop'))
async def stop(message: Message):
    await message.answer( "Остановка" )
    sys.exit(0)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет🎉! ��{message.from_user.first_name}�� бот для просмотра фильмов офлайн 💼.\n\n"
                         "Все пароли и логины не сохраняются\n\n"
                         "Данные остаются только в чате.\nВсе надежно 🪖",
                         reply_markup=kb_client_main)

@router.message(F.text == 'Вернуться в главное меню')
async def cancel_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы в главном меню", reply_markup=kb_client_main)


@router.message(F.text == 'Начать просмотр')
async def start_view(message: Message, state: FSMContext):
    await state.set_state(LogState.view)
    await message.answer("Отправьте ссылку на фильм или серию сериала",)

@router.message(LogState.view)
async def view(message: Message, state: FSMContext):
    await message.answer("Ссылка на фильм или серию сериала получена. Запуск фильма начинается. Выберите как войти",
                         reply_markup=kb_log_in)
    await state.update_data(url_mes=message.text)
    await state.set_state(LogState.login)


@router.message(LogState.login, (F.text == "По email/login") | (F.text == "По телефону"))
async def but_text(message: Message, state: FSMContext):
    if message.text == "По email/login":
        await message.answer(
            "Введите email/логин",
        )
        await state.set_state(LogState.email)
        print("email")
    elif message.text == "По телефону":
        await message.answer(
            "Введите телефон",
        )
        await state.set_state(LogState.phone)
        print("phone")


#Вход по майл
@router.message(LogState.email)
async def req_passw(message: Message, state: FSMContext):
    await state.update_data(email_mes=message.text)
    await message.answer("Введите пароль",)
    await state.set_state(LogState.passw)

@router.message(LogState.passw)
async def log_email_passw(message: Message, state: FSMContext):
    await state.update_data(pssw_mail=message.text)
    await state.set_state(LogState.code)
    await message.answer("Введите код подтверждения",)

@router.message(LogState.code)
async def one_time_code(message: Message, state: FSMContext):
    await state.update_data(one_code_mail=message.text)
    dt = await state.get_data()
    await message.answer(f"Данные для входа в яндекс аккаунт Mail - {dt['email_mes']}, Пароль - {dt['pssw_mail']}",)
    await state.clear()


#Вход по телефону
@router.message(LogState.phone)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введите код подтверждения",)
    await state.set_state(LogState.code_ph)
    
@router.message(LogState.code_ph)
async def phone_code(message: Message, state: FSMContext):
    await state.update_data(one_code_phone=message.text)
    await message.answer("Введите пароль",)
    await state.set_state(LogState.passw_phone)
    
@router.message(LogState.passw_phone)
async def phone_psw(message: Message, state: FSMContext):
    await state.update_data(pssw_phone=message.text)
    dt = await state.get_data()
    await message.answer(f"Данные для входа в яндекс аккаунт Телефон - {dt['phone']}, Пароль - {dt['pssw_phone']}",)
    selen
    await state.clear()