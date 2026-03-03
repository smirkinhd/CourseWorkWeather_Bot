import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import Config
from services.geocoder import GeocoderService
from services.weather import WeatherService
from handlers import MessageHandlers

class WeatherBot:
    """
    Главный класс бота, который объединяет все компоненты:
    - Конфигурацию
    - Сервисы (геокодер, погода)
    - Обработчики сообщений
    - Запуск и остановку бота
    """
    
    def __init__(self):
        """Инициализация бота и всех его компонентов"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Инициализация бота...")
        
        self.config = Config()
        
        self.bot = Bot(token=self.config.BOT_TOKEN)
        self.dp = Dispatcher()
        
        self.geocoder = GeocoderService(self.config.GEOCODING_URL)
        self.weather = WeatherService(
            self.config.WEATHER_URL, 
            self.config.WEATHER_PARAMS
        )
        
        self.handlers = MessageHandlers(self.geocoder, self.weather)
        
        self.dp.include_router(self.handlers.router)
        
        self.logger.info("Бот успешно инициализирован")
    
    async def set_commands(self):
        """Устанавливает команды бота в интерфейсе Telegram"""
        commands = [
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="help", description="Помощь")
        ]
        await self.bot.set_my_commands(commands)
        self.logger.info("Команды бота установлены")
    
    async def start(self):
        """Запускает бота"""
        self.logger.info("Бот запускается...")
        
        await self.set_commands()
        
        await self.dp.start_polling(self.bot)
    
    async def stop(self):
        """Останавливает бота и освобождает ресурсы"""
        self.logger.info("Бот останавливается...")
        
        await self.bot.session.close()
        
        await self.dp.storage.close()
        
        self.logger.info("Бот успешно остановлен")

def create_bot():
    """Фабрика для создания экземпляра бота"""
    return WeatherBot()