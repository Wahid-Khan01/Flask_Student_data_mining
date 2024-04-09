from flask import Blueprint

test = Blueprint('test', __name__)

@test.route('/test')
def testing():
    return "<a href='/gauth/login'><button>Google Login</button></a>"