from email_sender import EmailSender
from configurations import KafkaConfig

import json
import time
from datetime import datetime
from loguru import logger as log
from confluent_kafka import Consumer

class KafkaConsumer:   
    sender = EmailSender()
    months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]

    def read_messages(self):
        consumer = Consumer({'bootstrap.servers': KafkaConfig.KAFKA_SERVERS,
                             'group.id': KafkaConfig.CONSUMER_GROUP,
                             'auto.offset.reset': KafkaConfig.AUTO_OFFSET_RESET})
        consumer.subscribe([KafkaConfig.KAFKA_TOPIC])
        
        log.info("The connection to Kafka was successful")
        while True:
            message = consumer.poll(timeout=1.0)
            if message is None:
                time.sleep(1)
                continue

            log.info(f"resived message: {message}")
            try:
                message = json.loads(message.value().decode('utf-8'))
            except Exception as ex:
                log.info(f"Error on parsing message. Exeption {ex}")

            self.normalize_data(message)
            users = message.get("booking").get("staff")
            users.append(message.get("booking").get("owner"))

            for user in users:
                message["current_user"] = user
                self.sender.send_template_message("Обновление информации по бронированию", "template.html", message, user.get("username"))  

    def normalize_data(self, booking: dict):
        start_time_obj = datetime.fromisoformat(booking.get("booking").get("startTime").replace('Z', '+00:00'))
        end_time_obj = datetime.fromisoformat(booking.get("booking").get("endTime").replace('Z', '+00:00'))

        date = start_time_obj.date()

        booking["booking"]["startTime"] = start_time_obj.time().strftime('%H:%M')
        booking["booking"]["endTime"]   = end_time_obj.time().strftime('%H:%M')
        booking["booking"]["date"]      = f"{date.day} {self.months[date.month]} {date.year}"