from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from utils.auth import authenticate_user, create_access_token
from models.token_model import Token


ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(tags=["Authentication"])


@router.post("/token", response_model=Token)
async def token_request_endpoint(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
