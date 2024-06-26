from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger as log

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    chat_id = Column(Integer, primary_key=True)
    id = Column(Integer)
    username = Column(String)
    is_admin = Column(Boolean, default=False)

class Message(Base):
    __tablename__ = 'messages'

    booking_id = Column(Integer)
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    text = Column(String)

class UserManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///bot.db')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.User = User

    def add_user(self, chat_id, user_id, is_admin, username):
        try:
            session = self.Session()
            user = self.User(chat_id=chat_id, id=user_id, is_admin=is_admin, username=username)
            session.add(user)
            session.commit()
            session.close()
            log.info(f"Saved user whis data: {chat_id}, {user_id}, {is_admin}.")
        except:
            pass

    def find_user_by_id(self, user_id):
        session = self.Session()
        user = session.query(self.User).filter_by(id=user_id).first()
        session.close()
        return user

    def find_user_by_chat_id(self, chat_id):
        session = self.Session()
        user = session.query(self.User).filter_by(chat_id=chat_id).first()
        session.close()
        return user

    def find_by_username(self, username: str):
        session = self.Session()
        user = session.query(self.User).filter_by(username=username).first()
        session.close()
        return user

    def set_admin_status(self, user_id, is_admin):
        session = self.Session()
        user = session.query(self.User).filter_by(id=user_id).first()
        if user:
            user.is_admin = is_admin
            session.commit()
            log.info(f"set status is_admin={is_admin} by user with user_id={user_id}")
        session.close()

    def update_user_by_chat_id(self, chat_id, user_id, is_admin, username):
        session = self.Session()
        user = session.query(self.User).filter_by(chat_id=chat_id).first()
        if user:
            user.id = user_id
            user.is_admin = is_admin
            user.username = username
            session.commit()
        session.close()

    def get_admin_users(self):
        session = self.Session()
        admin_users = session.query(self.User).filter_by(is_admin=True).all()
        session.close()
        return admin_users

class MessageManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///bot.db')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.Message = Message

    def add_message(self, booking_id, message_id, chat_id, text):
        try:
            session = self.Session()
            message = self.Message(booking_id=booking_id, message_id=message_id, chat_id=chat_id, text=text)
            session.add(message)
            session.commit()
            session.close()
            log.info(f"Saved message whis data: {booking_id}, {message_id}, {chat_id}.")
        except:
            pass

    def find_message_by_message_id(self, message_id):
        session = self.Session()
        message = session.query(self.Message).filter_by(message_id=message_id).first()
        session.close()
        return message

    def find_messages_by_booking_id(self, booking_id):
        session = self.Session()
        messages = session.query(self.Message).filter_by(booking_id=booking_id).all()
        session.close()
        return messages

    def delete_messages_by_booking_id(self, booking_id):
        session = self.Session()
        session.query(self.Message).filter_by(booking_id=booking_id).delete()
        session.commit()
        session.close()
        log.info(f"Delited all messages whis booking_id: {booking_id}")
