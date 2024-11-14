from fastapi import APIRouter,Depends,HTTPException       #allow us to rout from out main.py file to our auth.py file
from pydantic import BaseModel
from models import Users
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import SessionLocal
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError                                                                   #javascript web token made of 3 parts (header, payload, signature)
from datetime import timedelta
from datetime import datetime,timezone

router=APIRouter(
    prefix='/auth',         #all the endpoints in this file will start with "/auth" automatically, es get_user avrà come endpoint"/auth/auth"
    tags=['auth']             #divides the function in this router from the ones in the other files in the swagger
)

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = '528d310738c18cbb287b1b6e62b37171c56ca8c307f508d1a0aabcf51ab71da4'
ALGORYTHM = 'HS256'

def get_db():
    db=SessionLocal()
    try:
        yield db            
    finally:
        db.close()      

def create_access_token(username: str, user_id: int, expires_delta : timedelta):
    encode= {'sub': username, 'id':user_id }
    expires= datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORYTHM)


db_dependency=Annotated[Session,Depends(get_db)]

class user_input(BaseModel):
    email: str
    username: str
    first_name : str
    last_name: str
    role: str
    password: str


class token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str,db):
    user=db.query(Users).filter(Users.username == username).first()
    if user==None:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return True


@router.post("/auth/",status_code=status.HTTP_201_CREATED)
async def get_user(db:db_dependency,create_user_request:user_input):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()


async def get_current_user(token:Annotated[str, Depends(OAuth2PasswordBearer)]):
    try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=ALGORYTHM)
        username: str =payload.get('sub')
        user_id: int =payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')


@router.post("/token")
async def login_for_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):                        #annotated: Simply, it is a way of saying that there is metadata x for the type T: Annotated[T, x]
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        return 'failed authentication'
    
    token=create_access_token(user.username,user.id,timedelta(minutes=20))

    return token

