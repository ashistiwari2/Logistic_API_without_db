from fastapi import FastAPI
from .database import engine
from . import model
from .routers import product
from .routers import seller, login



app=FastAPI(
    title="Products API",
    description="Get all details of product from website",
    terms_of_service="https://tamadoge.io/",
    contact={
        "Developer name":"Ashis Tiwari",
        "Website":"https://tamadoge.io/",
        "email":"ashistiwari2@gmail.com",
        "offical_email":"Ashis.Tiwari@in.ey.com"
    },
    license_info={
        'name':'Ashis',
        "url":"https://tamadoge.io/"
    },
    docs_url="/docs",redoc_url=None
)
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)
model.Base.metadata.create_all(engine)






