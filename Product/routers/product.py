from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import model
from typing import List
from .login import get_current_user
from ..import schema
from fastapi import status,Response,HTTPException
router=APIRouter(
    tags=["Products"],
    prefix="/product"
)

@router.get('/',response_model=List[schema.DisplayProduct])
            #tags=['Products'])
def product(db:Session=Depends(get_db),current_user:schema.Seller=Depends(get_current_user)):
    products=db.query(model.Product).all()
    return products
@router.get('/{id}',response_model=schema.DisplayProduct)
def product(id,response:Response,db:Session=Depends(get_db)):
    product=db.query(model.Product).filter(model.Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product Not Found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'Product not fOUND'}

    return product
@router.delete('/{id}')
def delete(id,db:Session=Depends(get_db)):
    db.query(model.Product).filter(model.Product.id==id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted '}

@router.put('t/{id}')
def update(id,request:schema.Product,db:Session=Depends(get_db)):
    product=db.query(model.Product).filter(model.Product.id==id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return {'Product succesfully updated'}


@router.post('/',status_code=status.HTTP_201_CREATED)
def add(request:schema.Product,db:Session=Depends(get_db)):
    new_product=model.Product(name=request.name,description=request.description,price=request.price,seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request