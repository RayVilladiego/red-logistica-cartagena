from fastapi import FastAPI
from login import router as login_router

app = FastAPI()

app.include_router(login_router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de gestión"}
