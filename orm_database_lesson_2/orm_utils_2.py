from passlib.context import CryptContext

pwd= CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password:str):
    password= pwd.hash(password)
    return password

def check_password(plain_password: str, hashed_password):
    result = pwd.verify(plain_password, hashed_password)
    return result
