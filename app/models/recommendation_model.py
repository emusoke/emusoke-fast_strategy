from typing import Dict, Any
from pydantic import BaseModel


class Strategy(BaseModel):
    compound_1: str
    compound_2: str
    pit_lap: int
    race_time: float


class Weather(BaseModel):
    current: Dict[str, Any]


class Recommendation(BaseModel):
    strategy: Strategy
    weather: Weather
