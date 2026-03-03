import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    
    WEATHER_PARAMS = {
        "current": ["temperature_2m", "relative_humidity_2m", "pressure_msl", 
                   "wind_speed_10m", "weathercode"],
        "timezone": "auto"
    }