import logging
import httpx
from typing import Optional, Tuple

class GeocoderService:
    """Сервис для поиска координат города через геокодер Open-Meteo"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
    
    async def get_coordinates(self, city_name: str) -> Optional[Tuple[float, float, str]]:
        """
        Получает координаты города по его названию
        Возвращает (lat, lon, display_name) или None
        """
        params = {
            "name": city_name,
            "count": 1,
            "language": "ru",
            "format": "json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                self.logger.info(f"Поиск координат для города: {city_name}")
                resp = await client.get(self.base_url, params=params, timeout=10)
                resp.raise_for_status()
                
                data = resp.json()
                if not data.get("results"):
                    self.logger.warning(f"Город не найден: {city_name}")
                    return None
                
                first = data["results"][0]
                
                display_name = f"{first.get('name', city_name)}"
                if first.get("country"):
                    display_name += f", {first['country']}"
                
                self.logger.info(f"Найдены координаты для {display_name}")
                return (first["latitude"], first["longitude"], display_name)
                
            except httpx.TimeoutException:
                self.logger.error("Таймаут при запросе к геокодеру")
                return None
            except httpx.HTTPStatusError as e:
                self.logger.error(f"HTTP ошибка геокодера: {e.response.status_code}")
                return None
            except Exception as e:
                self.logger.error(f"Неизвестная ошибка геокодера: {e}")
                return None