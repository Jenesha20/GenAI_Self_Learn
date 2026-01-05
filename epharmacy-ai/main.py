from fastapi import FastAPI
from api.chat_router import router

app = FastAPI(title="E-Pharmacy AI")

app.include_router(router)
