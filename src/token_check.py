from flask import request

from database.db_manager import DBManager

def needs_auth(func):
    def wrap(*args, **kwargs):
        if not "x-auth-token" in request.headers.keys():
            return {
                "error": "no token found on header!"
            }

        token = request.headers["x-auth-token"]
        assert DBManager.get().get_user_from_token(token)

        result = func(*args, **kwargs)

        return result
    wrap.__name__ = func.__name__
    return wrap
