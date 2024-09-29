from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, Depends, HTTPException, status
from .JWT import verify_token 
scheme=OAuth2PasswordBearer(tokenUrl="login")

def get_user(token: str= Depends(scheme)):
    try:
        payload=verify_token(token)
        return payload["sub"]
    except Exception as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token",
        )
