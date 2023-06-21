from pydantic import BaseModel


class Strategy_Request(BaseModel):
    laps: int
    location: str
