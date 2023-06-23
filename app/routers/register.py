from database.redis_db import get_redis_db
from fastapi import APIRouter, HTTPException
from models.user_model import User
from utils.auth import get_password_hash
from fastapi.encoders import jsonable_encoder


redis = get_redis_db()

router = APIRouter(prefix="/register", tags=["users"])


@router.post("/")
async def register_to_use_application(user: User):
    user_name = f"user:{user.username}"
    check = redis.json().get(user_name)
    if check is not None:
        raise HTTPException(status_code=400, detail="Username name taken.")
    user.password = get_password_hash(user.password)
    user_json = jsonable_encoder(user)
    try:
        redis.json().set(f"user:{user.username}", "$", user_json)
    except Exception as e:
        HTTPException(status_code=500, detail=e.args)
    return {"detail": f"Successfuly Registered. Your username is {user.username}"}
