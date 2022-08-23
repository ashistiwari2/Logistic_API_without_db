from fastapi import APIRouter
from ..database import get_db
from ..import schema,model
from sqlalchemy.orm import Session
from fastapi.params import Depends
from passlib.context import  CryptContext
router=APIRouter()
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

@router.post('/seller',response_model=schema.DisplaySeller,tags=['Seller'])
def create_seller(request:schema.Seller,db:Session=Depends(get_db)):
    hashpassword=pwd_context.hash(request.password)
    new_seller = model.Seller(username=request.username, email=request.email, password=hashpassword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
