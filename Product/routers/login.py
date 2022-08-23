from fastapi import  APIRouter,Depends,status,HTTPException
from ..import schema,database,model
from passlib.context import CryptContext
from ..database import get_db
from sqlalchemy.orm import Session
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..schema import TokenData
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY="07879d985286b033b946d042cb43d999202ce31516d41e36be68dbc9805a004f"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=20
def generate_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

router=APIRouter(
    tags=["Login"]
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    seller=db.query(model.Seller).filter(model.Seller.username==request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='username not found or invalid user')
    if not pwd_context.verify(request.password,seller.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail='Invalid password'
        )
    # use openssl rand -hex 32 to generate secret key
    access_token=generate_token(
        data={"sub":seller.username}
    )
    return {"access token":access_token,"token_type":"bearer"}

def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication",
        headers={'www-Authenticate':'Bearer'},
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data=TokenData(username=username)
    except JWTError:
        raise credentials_exception



