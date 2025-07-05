from telegram.ext import Application
from app.applog import get_logger
from app.settings import Config

TOKEN = Config.get_telegram_bot_key()  
logger = get_logger(f"[{Config.APP_NAME}]")

async def post_init(application: Application):
    """Función que se ejecuta después de que la aplicación se haya inicializado."""
    logger.info("🔗 Configurando el webhook del bot de Telegram...")
    await application.bot.delete_webhook(drop_pending_updates=True)