from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatType
from keyboards import moderation_keyboard
from config import MODERATION_CHAT_ID
from storage import moderation_map
from config import PUBLIC_CHANNEL_ID

router = Router()

# /start
@router.message(F.text == "/start", F.chat.type == ChatType.PRIVATE)
async def start(message: Message):
    await message.answer(
        "Отправьте свою историю, вопрос или ситуацию.\n\n"
        "Сообщение будет анонимно передано на модерацию."
    )

# приём истории
@router.message(F.chat.type == ChatType.PRIVATE)
async def receive_story(message: Message, bot: Bot):
    if not message.text:
        return

    # отправка в чат модерации
    sent = await bot.send_message(
        chat_id=MODERATION_CHAT_ID,
        text="📩 АНОНИМНОЕ СООБЩЕНИЕ:\n\n" + message.text,
        reply_markup=moderation_keyboard()
    )

    # сохраняем связь
    moderation_map[sent.message_id] = message.chat.id

    # подтверждение пользователю
    await message.answer(
        "Сообщение принято и отправлено на модерацию."
    )

# обработка модерации
@router.callback_query(F.data.in_(["approve", "reject"]))
async def moderate(callback: CallbackQuery, bot: Bot):
    msg = callback.message

    # защита от повторной модерации
    if msg.reply_markup is None:
        await callback.answer("Уже обработано", show_alert=True)
        return

    msg_id = msg.message_id
    user_chat_id = moderation_map.get(msg_id)

    approved = callback.data == "approve"

    if approved:
        # 1. убрать кнопки в чате модерации
        await msg.edit_reply_markup(reply_markup=None)

        # 2. публикация в публичный канал (НОВОЕ)
        await bot.send_message(
            chat_id=PUBLIC_CHANNEL_ID,
            text=msg.text
        )

        await callback.answer("Одобрено и опубликовано")

        # 3. уведомление пользователя
        if user_chat_id:
            await bot.send_message(
                chat_id=user_chat_id,
                text="Ваше сообщение прошло модерацию и опубликовано."
            )

    else:
        # НЕОДОБРЕНО → удалить
        await msg.delete()

        await callback.answer("Отклонено")

        if user_chat_id:
            await bot.send_message(
                chat_id=user_chat_id,
                text="Ваше сообщение не прошло модерацию."
            )

    moderation_map.pop(msg_id, None)
