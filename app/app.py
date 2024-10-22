from fastapi import FastAPI
from app.routers import pharmacy_router, user_router, product_router, request_router

app = FastAPI(name="API Diseño de Software")

app.include_router(pharmacy_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(request_router)

@app.get("/")
def is_running():
    return {"running": True}