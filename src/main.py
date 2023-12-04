from uuid import uuid4

from flask import Flask
from flask import request
from flask_cors import CORS

from database.db_manager import DBManager
from token_check import needs_auth

app = Flask(__name__)
CORS(app)

DBManager()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods = ["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]
    user = DBManager.get().get_user_from_username(username)
    if user and user.password == password:
        user.token = str(uuid4())
        DBManager.get().commit()
        return {
            "user_id": user.user_id,
            "token": user.token
        }

    print(username, password)
    return "Invalid username/password"

@app.route("/user", methods = ["POST"])
def user():
    name = request.json["username"]
    pw = request.json["password"]
    user_id = DBManager.get().add_user(name, pw)
    return {
        "user_id": user_id
    }

@app.route("/user/<int:user_id>", methods = ["GET"])
@needs_auth
def user_with_id(user_id: int):
    return DBManager.get().get_user_from_id(user_id).to_dict()

@app.route("/message", methods = ["POST"])
@needs_auth
def message():
    sender_id = request.json["sender_id"]
    receiver_id = request.json["receiver_id"]
    content = request.json["content"]
    DBManager.get().add_message(content, sender_id, receiver_id)
    return {
        "result": "OK"
    }

@app.route("/message/<int:user_id>", methods = ["GET"])
@needs_auth
def message_by_id(user_id: int):
    token = request.headers["x-access-token"]
    sender_id = DBManager.get().get_user_from_token(token).user_id
    return {
        "messages": DBManager.get().get_messages_from_chat(sender_id, user_id)
    }
