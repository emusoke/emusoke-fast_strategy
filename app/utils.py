from enum import Enum
import math
import requests
# from .. import
from .models.recommendation_model import Strategy, Weather, Recommendation


class Compound(Enum):
    SOFT = 1
    MEDIUM = 2
    HARD = 3


TEMP_FACTOR = {Compound.SOFT: 1/(3), Compound.MEDIUM: 1/(6**2), Compound.HARD: 1/(7**3)}
COMPOUND_BEST_LAP = {Compound.SOFT: 90, Compound.MEDIUM: 91, Compound.HARD: 92}


def degradation_factor(temp, compound):
    if temp < 1:
        temp = 1
    return round((temp * TEMP_FACTOR[compound]) + (math.log(temp, 10)), 2)


def lap_time(deg_factor, compound, lap):
    return COMPOUND_BEST_LAP[compound] + (deg_factor * ((lap**2)/1000))


def best_strategy(temp, laps):
    strategy_times = []
    for tire_1 in Compound:
        tire_1_deg_factor = degradation_factor(temp, tire_1)
        for tire_2 in Compound:
            tire_2_deg_factor = degradation_factor(temp, tire_2)
            if tire_1 != tire_2:
                for pit_stop in range(1, laps-1):
                    race_time = 0
                    for lap in range(0, laps+1):
                        if lap < pit_stop:
                            race_time += lap_time(tire_1_deg_factor, tire_1, lap)
                        else:
                            race_time += lap_time(tire_2_deg_factor, tire_2 ,lap)
                    strategy_times.append(Strategy(
                        compound_1=tire_1.name,
                        compound_2=tire_2.name,
                        pit_lap=pit_stop,
                        race_time=race_time
                        ))
    best_strategy = min(strategy_times, key=lambda strategy_times : strategy_times.race_time)
    return best_strategy


def celsius_convert(temp):
    return (temp - 32) * 5.0/9.0


def request_wrapper(City, laps):
    url = f"http://api.weatherstack.com/current?access_key=ENTERAPIKEY&query={City}"
    try:
        response = requests.request("GET", url)
        weather = Weather(current=response.json()['current'])
        temperature = weather.current['temperature']
        strategy = best_strategy(temperature,laps)
        recommendation = Recommendation(strategy=strategy,weather=weather)
        return recommendation
    except Exception as e:
        return e
    
