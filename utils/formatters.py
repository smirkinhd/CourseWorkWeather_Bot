from typing import Dict, Any

class WeatherFormatter:
    """Класс для форматирования данных погоды в читаемые сообщения"""
    
    WEATHER_CODES = {
        range(0, 2): ("ясно", "Ясно \U00002600"),
        2: ("облачно", "Облачно \U00002601"),
        3: ("пасмурно", "Пасмурно \U00002601"),
        range(45, 50): ("туман", "Туман \U0001F32B"),
        range(51, 68): ("морось/дождь", "Дождь \U00002614"),
        range(71, 78): ("снег", "Снег \U0001F328"),
        range(80, 83): ("ливень", "Дождь \U00002614"),
        range(95, 100): ("гроза", "Гроза \U000026A1")
    }
    
    @classmethod
    def get_weather_emoji(cls, code: int) -> str:
        """Преобразует код погоды WMO в эмодзи"""
        for key, value in cls.WEATHER_CODES.items():
            if isinstance(key, range) and code in key:
                return value[1]
            if code == key:
                return value[1]
        return "🌍"
    
    @classmethod
    def format_weather_message(cls, weather_data: Dict[str, Any], city_display: str) -> str:
        """Форматирует полное сообщение о погоде"""
        try:
            current = weather_data["current"]
            temp = current["temperature_2m"]
            humidity = current["relative_humidity_2m"]
            pressure = round(current["pressure_msl"] * 0.75006)  # гПа → мм рт. ст.
            wind = current["wind_speed_10m"]
            weather_emoji = cls.get_weather_emoji(current["weathercode"])
            
            return (
                f"🏙 **{city_display}**\n"
                f"🌡 **Температура:** {temp:.1f}°C {weather_emoji}\n"
                f"💧 **Влажность:** {humidity}%\n"
                f"📊 **Давление:** {pressure} мм рт. ст.\n"
                f"🌬 **Ветер:** {wind} км/ч"
            )
        except KeyError as e:
            return "⚠️ Ошибка при обработке данных погоды"