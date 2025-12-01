import jwt
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.exceptions import  AuthenticationFailed
from account.models import User

def token_generation(account):
    payload = {
    "user_id": account.id,
    "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def token_validation(token):
    try:        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")
    
    
def get_user_from_request(request):    
    token = request.headers.get("Authorization")
    if not token:
        raise AuthenticationFailed("Authorization header required")
    if " " in token:
        token = token.split(" ")[1]
    payload = token_validation(token)
    return payload["user_id"]    