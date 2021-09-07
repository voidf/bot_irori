import hashlib
from webcfg import salt, jwt_key
from jose import JWTError, jwt
from models.Auth import *


def encrypt(s: str) -> str:
    return hashlib.sha256((s + salt).encode('utf-8')).hexdigest().encode('utf-8')


def generate_jwt(adapter: Adapter):
    token_dict = {
        'id': str(adapter.pk)
    }
    return jwt.encode(
        token_dict,  # payload, 有效载体
        jwt_key,  # 进行加密签名的密钥
    )

def verify_jwt(token):
    try:
        payload = jwt.decode(token, jwt_key)
        adapter = Adapter.objects(pk=payload['id']).first()
        if not adapter:
            return None, "无此用户"
        return user, ""
    except:
        traceback.print_exc()
        return None, "数据错误"