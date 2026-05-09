
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "kirana-secret"

def generate_token(user_id):

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )
