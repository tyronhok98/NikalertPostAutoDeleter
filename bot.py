import asyncio
from datetime import datetime, timedelta

from telegram.ext import (
    ApplicationBuilder,
    ChannelPostHandler,
)

TOKEN = "8755172111:AAGgRZUMBc38YCmwiM8-Ka3zx5FX2NgMTUE"

messages_to_delete = []


async def handle_post(update, context):
    message = update.channel_post

    if not message:
        return

    text = message.text or ""

    if "\u26d4" in text:
        delete_time = datetime.now() + timedelta(hours=3)

        messages_to_delete.append({
            "chat_id": message.chat.id,
            "message_id": message.message_id,
            "delete_time": delete_time
        })

        print(f"Запланировано удаление: {message.message_id}")


async def delete_worker(app):
    while True:
        now = datetime.now()

        for msg in messages_to_delete[:]:
            if now >= msg["delete_time"]:
                try:
                    await app.bot.delete_message(
                        chat_id=msg["chat_id"],
                        message_id=msg["message_id"]
                    )

                    print(f"Удалено: {msg['message_id']}")

                except Exception as e:
                    print(e)

                messages_to_delete.remove(msg)

        await asyncio.sleep(60)


async def on_start(app):
    asyncio.create_task(delete_worker(app))


app = ApplicationBuilder().token(TOKEN).post_init(on_start).build()

app.add_handler(ChannelPostHandler(handle_post))

print("Бот запущен")

app.run_polling()