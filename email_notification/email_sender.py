import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, DictLoader
from jinja2 import Template
from loguru import logger as log

from configurations import EmailSenderConfig

class EmailSender:
    def __init__(self):
        self.env = Environment(loader=DictLoader({}))
        self.server = None
        self.open_session()

    def open_session(self):
        try:
            log.info("Попытка открыть SMTP сессию")
            self.server = smtplib.SMTP(EmailSenderConfig.SMTP_SERVER , EmailSenderConfig.SMTP_PORT, timeout=15)
            self.server.starttls()
            self.server.login(EmailSenderConfig.SMTP_USERNAME, EmailSenderConfig.SMTP_PASSWORD)
            log.info("SMTP session opened successfully")
        except Exception as e:
            log.error(f"Error opening SMTP session: {str(e)}")

    def send_email(self, subject, message_html, to_email):
        msg = MIMEMultipart()
        msg['From'] = EmailSenderConfig.SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        # Добавляем HTML-версию сообщения
        msg.attach(MIMEText(message_html, 'html'))

        try:
            if not self.server:
                self.open_session()
            self.server.send_message(msg)
            log.info("Email sent successfully")
        except Exception as e:
            log.info(f"Error sending email: {str(e)}")

    def close_session(self):
        if self.server:
            self.server.quit()
            log.info("SMTP session closed")

    def generate_html_from_string(self, data:dict):
        with open('template.html', 'r', encoding='utf-8') as file:
            template_string = file.read()

        template = Template(template_string)
        return template.render(data)
