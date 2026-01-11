from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def moderation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="ОДОБРЕНО",
                callback_data="approve"
            ),
            InlineKeyboardButton(
                text="НЕОДОБРЕНО",
                callback_data="reject"
            )
        ]
    ])
