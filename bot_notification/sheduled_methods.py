from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from loguru import logger as log

from database_managers import UserManager, MessageManager
from message_convertor import make_message
from kafka_listener import KafkaConsumer
from booking_connection import BookingConnection
from aiogram.enums import ParseMode


user_manager = UserManager()
message_manager = MessageManager()
kafka_consumer = KafkaConsumer()
booking_conection = BookingConnection()


# Метод вызываемый по расписанию (каждые 10 мин)
async def update_admins_list():
    booking_conection.update_admins_list()
    log.info("scheduller 'update_admins_list' executed.")

# Метод вызываемый по расписанию (каждые 10 сек)
async def read_messages_from_kafka(bot):
    counter = 0
    while True:
        message = kafka_consumer.get_message()
        if message is None:
            break

        if message.get("booking").get("status") == "REQUIRES_CONFIRMATION":
            await __send_message_to_admins(bot, *message)
        
        counter += 1
    log.info(f"scheduller 'read_messages_from_kafka' executed. {counter} messages processed.")

async def __send_message_to_admins(bot, booking_id, data:dict):
    message = make_message(data)

    for user in user_manager.get_admin_users():
        msg = await bot.send_message(user.chat_id, message, reply_markup=__makeKeyboard().as_markup())
        message_manager.add_message(booking_id=booking_id, message_id=msg.message_id, chat_id=msg.chat.id, text=message)

    log.info("The booking mailing was successful. Text=" + data)

def __makeKeyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Подтвердить бронирование",
        callback_data="yes"))
    builder.add(types.InlineKeyboardButton(
        text="Отменить бронирование",
        callback_data="no"))
    return builder