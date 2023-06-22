import redis
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from utils import request_wrapper
from models.strategy_request_model import strategy_request
import uvicorn
import os

redis_url = os.environ.get("REDIS_URL",'localhost')
redis = redis.Redis(host=redis_url, port=6379, decode_responses=True)

app = FastAPI()


@app.get("/{location}")
async def read_root(location: str):
    strategy = redis.json().get(location)
    return {"Result": strategy}


@app.post("/recommend")
async def recommend_activity(strategy_request: strategy_request):
    response = request_wrapper(strategy_request.location, strategy_request.laps)
    response_json = jsonable_encoder(response)
    try:
        redis.json().set(f"{strategy_request.location}", "$", response_json)
    except Exception as e:
        HTTPException(status_code=500,detail=e.args)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)