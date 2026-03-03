import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from services.geocoder import GeocoderService
from services.weather import WeatherService
from utils.formatters import WeatherFormatter

class MessageHandlers:
    """Класс-контейнер для обработчиков сообщений"""
    
    def __init__(self, geocoder: GeocoderService, weather: WeatherService):
        self.geocoder = geocoder
        self.weather = weather
        self.logger = logging.getLogger(__name__)
        self.router = Router()
        self._register_handlers()
    
    def _register_handlers(self):
        """Регистрирует все обработчики"""
        self.router.message.register(self.cmd_start, Command("start"))
        self.router.message.register(self.cmd_help, Command("help"))
        self.router.message.register(self.handle_city_message)
    
    async def cmd_start(self, message: Message):
        """Обработчик команды /start"""
        await message.answer(
            "👋 Привет! Я бот погоды.\n"
            "Просто напиши название города, и я покажу текущую погоду!"
        )
    
    async def cmd_help(self, message: Message):
        """Обработчик команды /help"""
        await message.answer(
            "🌤 **Как пользоваться:**\n"
            "• Отправь название города\n"
            "• Можно на любом языке\n"
            "• Например: Париж, Tokyo, Москва"
        )
    
    async def handle_city_message(self, message: Message):
        """Обработчик текстовых сообщений (названий городов)"""
        city = message.text.strip()
        if not city:
            return
        
        await message.bot.send_chat_action(message.chat.id, action="typing")
        
        coords = await self.geocoder.get_coordinates(city)
        if not coords:
            await message.reply("❌ Город не найден. Проверьте название.")
            return
        
        lat, lon, city_display = coords
        await message.answer(f"📍 Нашёл: {city_display}. Узнаю погоду...")
        
        weather_data = await self.weather.get_weather(lat, lon)
        if not weather_data:
            await message.reply("⚠️ Не удалось получить данные о погоде. Попробуйте позже.")
            return
        
        response = WeatherFormatter.format_weather_message(weather_data, city_display)
        await message.reply(response, parse_mode="Markdown")