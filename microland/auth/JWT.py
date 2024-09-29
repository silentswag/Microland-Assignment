from authlib.jose import JoseError
import jwt
import time

KEY="Anu"
def create_token(user_id: int):
    header={"alg":"HS256"}
    payload={
        "sub":user_id,
        "exp":int(time.time())+3600,
    }
    token=jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
    #token=jwt.encode(header, payload, KEY)
    return jwt.decode(token,"secret", algorithms=["HS256"])

def verify_token(token: str):
    try:
        decode=jwt.decode(token,KEY)
        decode.validate_exp()
        return decode
    except JoseError as e:
        raise Exception("Token validation fail") from e