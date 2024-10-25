from fastapi import FastAPI
from app.routers import pharmacy_router, user_router, product_router, request_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(name="API Diseño de Software")

app.include_router(pharmacy_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(request_router)

@app.get("/")
def is_running():
    return {"running": True}

# Permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)