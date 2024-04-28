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
        for attempt in range(3):    
            try:
                log.info(f"Попытка открыть SMTP сессию: {attempt+1}/3")
                self.server = smtplib.SMTP(EmailSenderConfig.SMTP_SERVER , EmailSenderConfig.SMTP_PORT, timeout=15)
                self.server.starttls()
                self.server.login(EmailSenderConfig.SMTP_USERNAME, EmailSenderConfig.SMTP_PASSWORD)
                log.info("SMTP session opened successfully")
                break;
            except Exception as e:
                log.error(f"Error opening SMTP session: {str(e)}")

    def send_email(self, title:str, message_html:str, to_email:str):
        msg = MIMEMultipart()
        msg['From'] = EmailSenderConfig.SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = title

        # Добавляем HTML-версию сообщения
        msg.attach(MIMEText(message_html, 'html'))

        if not self.server: 
            self.open_session()

        try:
            self.server.send_message(msg)
            log.info("Email sent successfully")
        except Exception as e:
            log.info(f"Error sending email: {str(e)}")
            self.open_session()

    def send_template_message(self, title:str, path_to_template:str, data:dict, to_email:str):
        message = self.__generate_html_from_string(path_to_template=path_to_template, data=data)
        self.send_email(title=title, message_html=message, to_email=to_email)

    def close_session(self):
        if self.server:
            self.server.quit()
            log.info("SMTP session closed")

    def __generate_html_from_string(self, path_to_template:str, data:dict):
        with open(path_to_template, 'r', encoding='utf-8') as file:
            template_string = file.read()

        template = Template(template_string)
        return template.render(data)
