from flask import request

from database.db_manager import DBManager

def needs_auth(func):
    def wrap(*args, **kwargs):
        if not "X-Auth-Token" in request.headers.keys():
            return {
                "error": "no token found on header!"
            }

        token = request.headers["X-Auth-Token"]
        usr = DBManager.get().get_user_from_token(token)
        if not usr:
            return {
                "error": "user with token not found!"
            }

        result = func(*args, **kwargs)

        return result
    wrap.__name__ = func.__name__
    return wrap
