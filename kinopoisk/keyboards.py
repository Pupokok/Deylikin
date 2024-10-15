from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_client_main = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text="Начать просмотр"),
        ],
        [
            KeyboardButton(text="🎁 Пригласить друга"),
            KeyboardButton(text="Обучение 🕹️")
        ],
        [
            KeyboardButton(text="���️ Настройки")
        ]

    ], 
    resize_keyboard=True,
    input_field_placeholder="Выберите действие из меню"
)
