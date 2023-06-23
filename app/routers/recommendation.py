from fastapi import APIRouter, HTTPException, Depends
from models.strategy_request_model import strategy_request
from utils.http_wrapper import request_wrapper
from fastapi.encoders import jsonable_encoder
from typing_extensions import Annotated
from typing import Any
from utils.auth import get_current_user

from database.redis_db import get_redis_db


redis = get_redis_db()


router = APIRouter(prefix="/recommend", tags=["Recommend"])


@router.post("/")
async def create_city_strategy_recommendation(
    request: strategy_request,
    current_user: Annotated[Any, Depends(get_current_user)],
):
    response = request_wrapper(request.location, request.laps)
    response_json = jsonable_encoder(response)
    try:
        redis.json().set(f"{request.location}", "$", response_json)
    except Exception as e:
        HTTPException(status_code=500, detail=e.args)
    return response
