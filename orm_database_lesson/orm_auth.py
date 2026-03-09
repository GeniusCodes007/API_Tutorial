
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import orm_models, orm_utils, orm_oauth2, orm_schemas
from orm_database import get_database

router = APIRouter(tags=['Authentication'],)


@router.post("/login", )#response_model=orm_schemas.Token)
def login_user(user_credential: OAuth2PasswordRequestForm= Depends(),db: Session= Depends(get_database)):

    # Check the database for the email passed
    loginUser_by_email = db.query(orm_models.User_Reg_Data).filter(orm_models.User_Reg_Data.email == user_credential.username).first()

    # Check the database for the username passed
    loginUser_by_username = db.query(orm_models.User_Reg_Data).filter(orm_models.User_Reg_Data.username == user_credential.username).first()

    # Validate, if found
    if loginUser_by_email :
        work_with = loginUser_by_email
    elif loginUser_by_username:
        work_with = loginUser_by_username
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect Email or Password")

    # Check password
    if not orm_utils.check_password(plain_password=user_credential.password, hashed_password=work_with.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Access Denied")



    # Create a token
    my_user_token = orm_oauth2.create_token(data={"access_type": "user",
                                             "user_id":work_with.id,
                                             "username": work_with.username,
                                             "email": work_with.email})

    return {"access_token":my_user_token,"token_type":"bearer"},
