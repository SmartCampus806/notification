BOT_TOKEN = '6635344842:AAHZv4PxMSjiNnrBH4nvOCtUe7Fm_bVyF9E'
KAFKA_SERVERS = 'localhost:9092'
CONSUMER_GROUP = 'bot'
KAFKA_TOPIC = 'notifications'
JWT_SECRET = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

class RoomBookingConfiguration:
    __room_booking_host="172.28.16.1"
    __room_booking_port="8000"

    auth_url       = f"http://{__room_booking_host}:{__room_booking_port}/api/auth/login"
    admin_list_url = f"http://{__room_booking_host}:{__room_booking_port}/api/user/admins"
    set_status_url = f"http://{__room_booking_host}:{__room_booking_port}/api/bookings/status"

    username = "notification@bot.ru"
    password = "root"