import jwt
from core import secret_key



def get_user_id_from_token(token):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        print(decoded_token)
        user_id = decoded_token['id']
        print(user_id)
        return user_id
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None