from pydantic import BaseModel, validator
from fastapi import HTTPException


class strategy_request(BaseModel):
    laps: int
    location: str

    @validator('laps')
    def valid_laps(cls,l):
        if not 20 <= l <= 80:
            raise HTTPException(status_code=400,
                                detail="Race should be between 20 and 80 laps")
        return l
