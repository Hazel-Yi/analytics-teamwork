from functools import wraps
import jwt
from flask import Flask, request
from flask_restplus import abort


secret_key = "secret"


class AuthenticationToken:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_token(self):
        info = {'username': 'admin'}
        return jwt.encode(info, self.secret_key, algorithm='HS256')

    def validate_token(self, token):
        info = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        return True


auth = AuthenticationToken(secret_key)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')

        try:
            user = auth.validate_token(token)
        except Exception as e:
            abort(401, e)

        return f(*args, **kwargs)

    return decorated
