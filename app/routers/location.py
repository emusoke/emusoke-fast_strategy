from database.redis_db import get_redis_db
from fastapi import APIRouter, Depends
from utils.auth import get_current_user
from typing_extensions import Annotated
from typing import Any


redis = get_redis_db()

router = APIRouter(prefix="/location", tags=["location"])


@router.get("/{location}")
async def get_city_strategy(
    location: str, current_user: Annotated[Any, Depends(get_current_user)]
):
    strategy = redis.json().get(location)
    return {"Result": strategy}
