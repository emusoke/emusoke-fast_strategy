import logging
import requests
import os
from models.recommendation_model import Weather, Recommendation
from fastapi import HTTPException
from dotenv import load_dotenv
from utils.simulation import best_strategy

load_dotenv()


def request_wrapper(city, laps):
    api_key = os.getenv("API_KEY")
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
    try:
        response = requests.request("GET", url)
        if "error" in response.json().keys():
            raise HTTPException(
                status_code=400, detail={"info": response.json()["error"]["type"]}
            )
        weather = Weather(current=response.json()["current"])
        temperature = weather.current["temperature"]
        strategy = best_strategy(temperature, laps)
        recommendation = Recommendation(strategy=strategy, weather=weather)
        return recommendation
    except Exception as e:
        logging.error(f"Error-{e}-Request: for {city} failed")
        raise (e)
