from loguru import logger as log
import requests
import time
import jwt

from datetime import datetime

from configuration import RoomBookingConfiguration as conf


class BookingConnection:
    jwt_token = None
    expiration_time = None

    async def __ini__(self): 
        await self.check_authorise()

    async def update_admins_list(self):
        await self.check_authorise()
        response = requests.get(conf.admin_list_url, headers={"Authorization": f"Bearer {self.jwt_token}"})
        if response.status_code != 200:
            log.error(f"Ошибка HTTP при обновлении списка администраторов. {response.text}")
            return None
        return response.json()

    async def change_status(self, booking_id: int, status:str):
        await self.check_authorise()
        bar = f"Bearer {self.jwt_token}"
        log.info(bar)
        response = requests.put(conf.set_status_url, 
                                 headers={"Authorization": bar},
                                 params={"bookingId": booking_id, "status": status})
        if response.status_code != 200:
            log.error(f"Ошибка обновления статуса бронирования {booking_id}, запрос к RoomBooking не был выполнен успешно. Статус код: {response.status_code}, ответ: {response.text}")
            return False
        return True
    
    async def autorise(self):
        response = requests.post(conf.auth_url, json={"username": conf.username, "password": conf.password})
        if response.status_code != 200:
            log.error(f"Авторизация прошла неудачно. Код ответа: {response.status_code}, сообщение: {response.text}")
        log.info(f"Авторизация сервиса прошла успешно.")
        
        self.jwt_token = response.json().get("token")
        if self.jwt_token is None:
            log.error(f"Ошибка получения JWT токена. Полученное сообщение: {response.text}")

        decoded_jwt = jwt.decode(self.jwt_token, options={"verify_signature": False})
        self.expiration_time = decoded_jwt.get("exp")
        log.info(f"Дата истечения токена: {datetime.fromtimestamp(self.expiration_time)}")

    async def authorise_user(self, username, password):
        response = requests.post(conf.auth_url, json={"username": username, "password": password})
        if response.status_code != 200:
            log.error(f"Авторизация прошла неудачно. Код ответа: {response.status_code}, сообщение: {response.text}")
        log.info(f"Авторизация пользователя прошла успешно.")
        
        user = response.json().get("user")
        if user is None:
            log.error(f"Ошибка получения пользователя. Полученное сообщение: {response.text}")
        return user

    async def check_authorise(self):
        if self.jwt_token is None: await self.autorise()
        if self.expiration_time is None: await self.autorise()
        elif self.expiration_time <= int(time.time()):
            log.info("Время жизни токена истекло. Производится запрос нового токена.")
            await self.autorise()