import logging
import sys
from pathlib import Path
from .config import settings
from datetime import datetime

# Create logs directory
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

class Logger:    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str = "LOG"):
        if name not in cls._loggers:
            cls._loggers[name] = cls._setup_logger(name)
        return cls._loggers[name]
    
    @staticmethod
    def _setup_logger(name: str):
        logger = logging.getLogger(name)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
            
        logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        logger.propagate = False
        
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        if not settings.DEBUG:
            file_handler = logging.FileHandler(
                LOG_DIR / f"LOG_{datetime.now().strftime('%Y-%m-%d')}.log",
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger

app_logger = Logger.get_logger("LOG.app")
db_logger = Logger.get_logger("SAV.db")
api_logger = Logger.get_logger("LOG.api")