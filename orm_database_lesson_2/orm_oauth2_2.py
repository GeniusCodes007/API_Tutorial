from jose import jwt, JWTError
from datetime import datetime, timedelta
import orm_database_2
from orm_database_lesson_2.my_models import orm_models_2
from orm_database_lesson_2.my_schemas import orm_schemas_2
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from config_2 import my_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# When creating our token, we need three things
#-> Secret Key
#-> Algorithm= HS256
#-> Expiration Time
# 7: 39: 21

SECRET_KEY = f"{my_settings.secret_key}"
ALGORITHM = f"{my_settings.algorithm}"
EXPIRES_IN_MINUTES = my_settings.access_token_expire_minutes

def create_token(data: dict):
    encoded_data = data.copy()

    expiry_time= datetime.now().astimezone() + timedelta(minutes=EXPIRES_IN_MINUTES)
    #encoded_data["exp"] = expiry_time
    encoded_data.update({"exp": expiry_time})

    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        my_id = payload.get("user_id")
        if my_id is None:
            raise credentials_exception

        token_data = orm_schemas_2.TokenResponse(access_token=token, token_type="bearer", token_id=str(my_id))
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(orm_database_2.get_database)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_token(token, credentials_exception)

    user=db.query(orm_models_2.User_Reg_Data).filter(orm_models_2.User_Reg_Data.id == token.token_id).first()


    return user

