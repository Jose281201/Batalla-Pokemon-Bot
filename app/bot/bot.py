from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, ConversationHandler
)

from app.bot.commands_register import register_commands
from app.bot.utils import post_init
from app.applog import get_logger
from app.settings import Config

TOKEN = Config.get_telegram_bot_key()  
logger = get_logger(f"[{Config.APP_NAME}]")

def main():
    """Función principal del bot"""

    logger.info("🔗 Iniciando el bot de Telegram...")
    
    # Verifica que el token esté 
    if not TOKEN:
        logger.error("❌ No se encontró TELEGRAM_BOT_KEY en las variables de entorno")
        raise ValueError("Token de Telegram no configurado")
    else:
        logger.info("✅ Token de Telegram encontrado")
    
    app = ApplicationBuilder().token(Config.TELEGRAM_BOT_KEY).post_init(post_init).build()

    register_commands(app)

    logger.info("Bot corriendo. ¡Inicia la batalla en Telegram con /start!")
    app.run_polling()