from passlib.context import CryptContext

pwd= CryptContext(schemes=["pbkdf2_sha256"],deprecated="auto")

def hash_pass(password: str):
    return pwd.hash(password)

def verify_pass(original_pwd: str, hashed_pwd: str):
    return pwd.verify(original_pwd,hashed_pwd)