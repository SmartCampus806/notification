from kafka_consumer import KafkaConsumer


if __name__ == "__main__":
    listener = KafkaConsumer()
    listener.read_messages()
