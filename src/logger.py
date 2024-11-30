import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from src.config import config

def setup_logger(name: str = "career_scout") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)

    # Форматирование логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Обработчик для записи в файл с ротацией
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Создаем глобальный логгер
logger = setup_logger() 