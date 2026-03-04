# Телеграм-бот "Прогноз погоды"

Телеграм-бот для курсовой работы

## Архитектура 

- bot.py — управление ботом
- handlers.py — логика ответов
- services/ — бизнес-логика
- main.py — точка входа

```mermaid
graph TB
    subgraph "Telegram"
        TG[Telegram API]
        User[Пользователь]
    end
    
    subgraph "Ядро бота"
        WB[WeatherBot<br/>main.py]
        C[Config<br/>config.py]
    end
    
    subgraph "Обработчики"
        MH[MessageHandlers<br/>handlers.py]
    end
    
    subgraph "Сервисы"
        GEO[GeocoderService<br/>geocoder.py]
        WTH[WeatherService<br/>weather.py]
    end
    
    subgraph "Утилиты"
        FMT[WeatherFormatter<br/>formatters.py]
    end
    
    subgraph "Внешние API"
        GM[Open-Meteo Geocoding<br/>geocoding-api.open-meteo.com]
        WM[Open-Meteo Weather<br/>api.open-meteo.com]
    end
    
    User <-->|Сообщения| TG
    TG <-->|Polling| WB
    WB -->|Инициализирует| C
    WB -->|Создает| MH
    WB -->|Создает| GEO
    WB -->|Создает| WTH
    
    MH -->|Вызывает| GEO
    MH -->|Вызывает| WTH
    MH -->|Использует| FMT
    
    GEO -->|HTTP GET| GM
    WTH -->|HTTP GET| WM
    
```

## Библиотеки

- aiogram==3.26.0
- httpx==0.28.1

## Запуск проекта

- Клонировать репозиторий
  
```bash
git clone https://github.com/yourusername/weather-bot.git
cd weather-bot
```

- Создать .env файл и разместить следующее
  
```
BOT_TOKEN=ваш токен
```

- Установить зависимости
```bash
pip install -r requirements.txt
```

- Запустить проект

```bash
python main.py
```
