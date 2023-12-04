"""Module for managing the database"""

# pylint: disable=E0401, R0402

from threading import Lock

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from .model import Base, User, Message

# pylint: disable=R0801

class DBManager():
    """Class that manages the database"""

    def __init__(self):
        if DBManager.get() is not None:
            return DBManager.get()

        db_connection = sqlalchemy.create_engine(f"sqlite:///{self._dbfile}",
                                                 connect_args={'check_same_thread': False})
        Base.metadata.create_all(db_connection)

        session_factory = sessionmaker(db_connection, autoflush=False)
        _session = scoped_session(session_factory)
        self.session = _session()

        DBManager._inst = self

    _inst = None
    lock = Lock()
    _dbfile = "src/database/database.sqlite"

    @staticmethod
    def get():
        return DBManager._inst

    def add_message(self, content, sender_id, receiver_id) -> int:
        with self.lock:
            sender = self.get_user_from_id(sender_id)
            receiver = self.get_user_from_id(receiver_id)

            message = Message(content=content)
            sender.sent_messages.append(message)
            receiver.received_messages.append(message)
            self.session.add(message)

        self.commit()

        return message.message_id

    def add_user(self, username, password) -> int:
        with self.lock:
            user_obj = User(username=username, password=password)
            self.session.add(user_obj)

        self.commit()

        return user_obj.user_id

    def commit(self) -> None:
        """Commits changes to database"""

        with self.lock:
            try:
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("Committing database changes failed, rolling back")
                self.session.rollback()

    def get_message_from_id(self, message_id: int) -> Message | None:
        return self.session.query(Message).filter(Message.message_id==message_id).first()

    def get_messages_from_chat(self, user1_id: int, user2_id: int) -> list[Message] | None:
        resp = []

        for msg in self.session.query(Message).filter(Message.sender_id==user1_id and Message.receiver_id==user2_id):
            resp.append(msg.to_dict())
        for msg in self.session.query(Message).filter(Message.sender_id==user2_id and Message.receiver_id==user1_id):
            resp.append(msg.to_dict())

        return resp

    def get_user_from_username(self, username: str) -> User | None:
        return self.session.query(User).filter(User.username==username).first()

    def get_user_from_id(self, user_id: int) -> User | None:
        return self.session.query(User).filter(User.user_id==user_id).first()

    def get_user_from_token(self, token: str) -> User | None:
        return self.session.query(User).filter(User.token==token).first()
