"""Declaring data models"""

import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.hybrid import hybrid_property

Base = sqlalchemy.ext.declarative.declarative_base()

# pylint: disable=R0903

class User(Base):
    """User representation."""

    __tablename__ = "user"
    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    token = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", cascade="all,delete", uselist=True)
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", cascade="all,delete", uselist=True)

    def to_dict(self):
        return {
            "username": self.username
        }

class Message(Base):
    """Message representation."""

    __tablename__ = "message"
    message_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    receiver_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("user.user_id"))
    sender_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("user.user_id"))

    def to_dict(self):
        return {
            "sender_id": self.sender_id,
            "received_id": self.receiver_id,
            "content": self.content
        }
