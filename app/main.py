from routers import location, recommendation, token, register
from fastapi import FastAPI

app = FastAPI()

app.include_router(location.router)
app.include_router(recommendation.router)
app.include_router(register.router)
app.include_router(token.router)
