import logging
import httpx
from typing import Optional, Dict, Any

class WeatherService:
    """Сервис для получения погоды по координатам"""
    
    def __init__(self, base_url: str, default_params: Dict[str, Any]):
        self.base_url = base_url
        self.default_params = default_params
        self.logger = logging.getLogger(__name__)
    
    async def get_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Получает текущую погоду по координатам
        Возвращает словарь с данными или None
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            **self.default_params
        }
        
        async with httpx.AsyncClient() as client:
            try:
                self.logger.info(f"Запрос погоды для координат: {lat}, {lon}")
                resp = await client.get(self.base_url, params=params, timeout=10)
                resp.raise_for_status()
                
                data = resp.json()
                if "current" not in data:
                    self.logger.warning("Ответ не содержит данных о текущей погоде")
                    return None
                
                return data
                
            except httpx.TimeoutException:
                self.logger.error("Таймаут при запросе к weather API")
                return None
            except httpx.HTTPStatusError as e:
                self.logger.error(f"HTTP ошибка weather API: {e.response.status_code}")
                return None
            except Exception as e:
                self.logger.error(f"Неизвестная ошибка weather API: {e}")
                return None