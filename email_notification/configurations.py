class KafkaConfig:
    KAFKA_SERVERS = 'localhost:9092'
    CONSUMER_GROUP = 'email'
    KAFKA_TOPIC = 'email'
    AUTO_OFFSET_RESET = 'earliest'

class EmailSenderConfig:
        SMTP_SERVER = 'smtp.mai.education'
        SMTP_PORT = 587
        SMTP_USERNAME = 'AMBulovyatov'
        SMTP_PASSWORD = 'GMJkMZ7o'
        SENDER_EMAIL = 'ambulovyatov@mai.education'