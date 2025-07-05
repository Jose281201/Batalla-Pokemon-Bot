import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

class Config:
    """Clase de configuración del proyecto"""
    TELEGRAM_BOT_KEY: str = os.getenv("TELEGRAM_BOT_KEY")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    APP_NAME: str = os.getenv("APP_NAME", "PokemonBattleBot")
    AUTHOR_NAME: str = os.getenv("AUTHOR_NAME", "José Luis")

    @classmethod
    def get_telegram_bot_key(cls) -> str:
        """Devuelve la key del bot de Telegram."""
        return cls.TELEGRAM_BOT_KEY
    
    @classmethod
    def get_app_name(cls) -> str:
        """Devuelve el nombre de la aplicación."""
        return cls.APP_NAME
    
    @classmethod
    def get_author_name(cls) -> str:
        """Devuelve el nombre del autor de la aplicación."""
        return cls.AUTHOR_NAME

    @classmethod
    def load_all(cls) -> Dict[str,str]:
        """Carga todos los valores configurables."""
        return {
            "app":          cls.get_app_name(),
            "author":       cls.get_author_name(),
            "telegram_key": cls.get_telegram_bot_key()
        }