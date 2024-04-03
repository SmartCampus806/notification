from configuration import KAFKA_SERVERS, CONSUMER_GROUP, KAFKA_TOPIC
from confluent_kafka import Consumer
import json
from loguru import logger as log

class KafkaConsumer:
    def __init__(self):
        self.consumer = Consumer({'bootstrap.servers': KAFKA_SERVERS,
                     'group.id': CONSUMER_GROUP,
                     'auto.offset.reset': 'earliest'})
        self.consumer.subscribe([KAFKA_TOPIC])
    
    def get_message(self):
        message = self.consumer.poll(timeout=1.0)
        if message is None:
            return None
        try:
            message = json.loads(message.value().decode('utf-8'))
        except: 
            log.error(f"Unvalid data. Resived message: {message}")
            return None
        
        booking_id = message.get('booking_id')
        text = message.get('text')
        if booking_id is None or text is None:
            log.error(f"booking_id or text is undefined. Resived: {message.value().decode('utf-8')}")
            return None
        log.info(f"Resived message: {message}")
        return (booking_id, text)