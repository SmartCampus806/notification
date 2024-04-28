import asyncio
from loguru import logger as log
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database_managers import UserManager, MessageManager
from configuration import BOT_TOKEN
from sheduled_methods import read_messages_from_kafka, update_admins_list
from booking_connection import BookingConnection
import base64


user_manager = UserManager()
message_manager = MessageManager()
booking_connection = BookingConnection()
# Настройка бот
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
        

# Обработка команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    username = base64.b64decode(message.text.replace("/start ", "")).decode('utf-8')
    user_manager.add_user(message.from_user.id, None, False, username=username)
    await message.answer("Привет! введи пароль от своего аккаунта SmartCampus для получения доступа к сервису")

@dp.message()
async def password(message: types.Message):
    chat_id = message.from_user.id
    username = user_manager.find_user_by_chat_id(chat_id=chat_id).username
    password = message.text
    user = await booking_connection.authorise_user(username=username, password=password)
    if user is not None:
        user_manager.update_user_by_chat_id(chat_id=chat_id, user_id=user.get("id"), is_admin=user.get("role")=="ADMINISTRATOR", username=username)
        await message.answer(user.get("fullName") + ", добро пожаловать!!!")
    else:
        await message.answer("Кажется вы ошиблись в пароле, давай попробуем еще раз.")


# Обработка нопки отменить бронирование
@dp.callback_query(lambda c: c.data == 'no')
async def edit_message_callback(callback_query: types.CallbackQuery):
    saved_message = message_manager.find_message_by_message_id(callback_query.message.message_id)
    if saved_message is None: return;

    if await booking_connection.change_status(saved_message.booking_id, "REJECTED") is False:
        await bot.send_message(callback_query.message.user.chat_id, "Не удалось изменить статус бронирования, сервер не отвечает")

    messages = message_manager.find_messages_by_booking_id(saved_message.booking_id)
    for message in messages:
        await bot.edit_message_text(chat_id    = message.chat_id,
                                    message_id = message.message_id,
                                    text       = message.text + "\n Бронирование отменено")
    message_manager.delete_messages_by_booking_id(saved_message.booking_id)

# Обработка нопки отменить бронирование
@dp.callback_query(lambda c: c.data == 'yes')
async def edit_message_callback(callback_query: types.CallbackQuery):
    saved_message = message_manager.find_message_by_message_id(callback_query.message.message_id)
    if saved_message is None: return;

    if await booking_connection.change_status(saved_message.booking_id, "CONFIRMED") is False:
        await bot.send_message(callback_query.message.user.chat_id, "Не удалось изменить статус бронирования, сервер не отвечает")

    messages = message_manager.find_messages_by_booking_id(saved_message.booking_id)
    for message in messages:
        await bot.edit_message_text(chat_id    = message.chat_id,
                                    message_id = message.message_id,
                                    text       = message.text + "\n Бронирование подтверждено")
    message_manager.delete_messages_by_booking_id(saved_message.booking_id)


## MAIN
async def main():
    scheduler = AsyncIOScheduler(standalone=True)
    scheduler.add_job(read_messages_from_kafka, args=(bot,), trigger='interval', seconds=10, misfire_grace_time=None)
    scheduler.add_job(update_admins_list, trigger='interval', seconds=30, misfire_grace_time=None)
    scheduler.start()
    log.info("Scheduler started")
    log.info("Bot started")
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())
