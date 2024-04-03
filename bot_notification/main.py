import asyncio
from loguru import logger as log

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database_managers import UserManager, MessageManager
from configuration import BOT_TOKEN
from sheduled_methods import read_messages_from_kafka, update_admins_list
from booking_connection import BookingConnection

user_manager = UserManager()
message_manager = MessageManager()
booking_connection = BookingConnection()
# Настройка бот
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
        

# Обработка команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    user_manager.add_user(message.from_user.id, None, True)
    await message.answer("Привет! Рады тебя видеть")

# Обработка нопки отменить бронирование
@dp.callback_query(lambda c: c.data == 'no')
async def edit_message_callback(callback_query: types.CallbackQuery):
    saved_message = message_manager.find_message_by_message_id(callback_query.message.message_id)
    if saved_message is None: return;

    messages = message_manager.find_messages_by_booking_id(saved_message.booking_id)
    for message in messages:
        await bot.edit_message_text(chat_id    = message.chat_id,
                                    message_id = message.message_id,
                                    text       = message.text + "\n Бронирование отменено")
    message_manager.delete_messages_by_booking_id(saved_message.booking_id)
    booking_connection.change_status(saved_message.booking_id, "no") #TODO: изменит на реальный статус

# Обработка нопки отменить бронирование
@dp.callback_query(lambda c: c.data == 'yes')
async def edit_message_callback(callback_query: types.CallbackQuery):
    saved_message = message_manager.find_message_by_message_id(callback_query.message.message_id)
    if saved_message is None: return;

    messages = message_manager.find_messages_by_booking_id(saved_message.booking_id)
    for message in messages:
        await bot.edit_message_text(chat_id    = message.chat_id,
                                    message_id = message.message_id,
                                    text       = message.text + "\n Бронирование подтверждено")
    message_manager.delete_messages_by_booking_id(saved_message.booking_id)
    booking_connection.change_status(saved_message.booking_id, "yes") #TODO: изменит на реальный статус

## MAIN
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(read_messages_from_kafka, args=(bot,), trigger='interval', seconds=10)
    scheduler.add_job(update_admins_list, trigger='interval', seconds=600)
    scheduler.start()
    log.info("Scheduler started")
    log.info("Bot started")
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())
