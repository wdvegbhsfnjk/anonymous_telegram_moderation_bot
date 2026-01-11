# Anonymous Telegram Moderation Bot

Telegram-бот на Python (aiogram 3.x) для сбора анонимных сообщений от пользователей,
модерации в закрытой группе и публикации одобренных сообщений в публичный канал.

---

## Функциональность

- Приём анонимных сообщений в личных сообщениях бота
- Передача сообщений в закрытый чат модерации
- Inline-модерация:
  - ОДОБРЕНО — сообщение остаётся в чате и публикуется в публичный канал
  - НЕ ОДОБРЕНО — сообщение удаляется
- Уведомление пользователя о результате модерации
- Полное отсутствие публичных идентификаторов пользователя

---

## Архитектура потока

Пользователь (Private Chat)
↓
Бот
↓
Закрытая группа модерации
↓
(ОДОБРЕНО)
↓
Публичный канал

---

## Стек технологий

- Python ≥ 3.10
- aiogram 3.x
- python-dotenv

---

## Структура проекта

├── bot.py # точка входа
├── handlers.py # обработчики сообщений и модерации
├── keyboards.py # inline-клавиатуры
├── config.py # загрузка конфигурации
├── storage.py # in-memory хранилище соответствий
├── requirements.txt
├── .gitignore
└── README.md


---

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/wdvegbhsfnjk/anonymous_telegram_moderation_bot.git
cd anonymous_telegram_moderation_bot

Виртуальное окружение
python -m venv .venv
source .venv/bin/activate

Установка зависимостей
pip install -r requirements.txt

Конфигурация
Создать файл .env в корне проекта:
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
MODERATION_CHAT_ID=-100XXXXXXXXXX
PUBLIC_CHANNEL_ID=-100XXXXXXXXXX

Запуск
python bot.py
