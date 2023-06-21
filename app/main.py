import redis
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from .utils import request_wrapper
from .models.strategy_request_model import Strategy_Request


redis = redis.Redis(host='redis', port=6379, decode_responses=True)

app = FastAPI()


@app.get("/{location}")
async def read_root(location: str):
    strategy = redis.json().get(location)
    return {"Result": strategy}


@app.post("/recommend")
async def recommend_activity(strategy_request: Strategy_Request):
    response = request_wrapper(strategy_request.location,strategy_request.laps)
    response_json = jsonable_encoder(response)
    redis.json().set(f'{strategy_request.location}', '$', response_json)
    return response