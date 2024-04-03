from email_sender import EmailSender
from configurations import KafkaConfig

import json
import time
from loguru import logger as log
from confluent_kafka import Consumer

class KafkaConsumer:   
    sender = EmailSender()
    
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
            try:
                message = json.loads(message.value().decode('utf-8'))
                template = message['template']
                data     = message['data']
                to       = message['to']
                title    = message['title']
                

                result = self.sender.generate_html_from_string(template, data)
                log.info(f"Message from kafka resived. HTML data: {result}")
                self.sender.send_email(title, result, to)
                
            except:
                log.info(f'Error on parsing message. Message: {message.value().decode('utf-8')}')