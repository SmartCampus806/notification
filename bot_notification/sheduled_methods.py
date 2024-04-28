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


# Обновление списка администраторов с BookingService
async def update_admins_list():
    valid_admins = set([admin.get("id") for admin in await booking_conection.update_admins_list()])
    saved_admins = set([admin.id for admin in user_manager.get_admin_users()])

    for admin in list(saved_admins - valid_admins):
        user = user_manager.find_user_by_id(admin)
        if user is not None: user_manager.set_admin_status(user_id=admin, is_admin=False)

    for admin in list(valid_admins - saved_admins):
        user = user_manager.find_user_by_id(admin)
        if user is not None: user_manager.set_admin_status(user_id=admin, is_admin=True)

    log.info("Список администраторов" + ", ".join([user.username for user in user_manager.get_admin_users()]))

    log.info("scheduller 'update_admins_list' executed.")

# Чтение пула сообщений из Kafka
async def read_messages_from_kafka(bot):
    counter = 0
    while True:
        message = kafka_consumer.get_message()
        if message is None:
            break

        if message.get("booking").get("status") == "REQUIRES_CONFIRMATION":
            await __send_message_to_admins(bot, message)
        
        counter += 1
    log.info(f"scheduller 'read_messages_from_kafka' executed. {counter} messages processed.")

async def __send_message_to_admins(bot, data:dict):
    message = make_message(data)

    for user in user_manager.get_admin_users():
        msg = await bot.send_message(user.chat_id, message, reply_markup=__makeKeyboard().as_markup())
        message_manager.add_message(booking_id=data.get('booking').get("id"),
                                    message_id=msg.message_id,
                                    chat_id=msg.chat.id,
                                    text=message)

    log.info("The booking mailing was successful. Text=" + message)

def __makeKeyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Подтвердить бронирование",
        callback_data="yes"))
    builder.add(types.InlineKeyboardButton(
        text="Отменить бронирование",
        callback_data="no"))
    return builder