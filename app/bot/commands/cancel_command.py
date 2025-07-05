from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (ContextTypes, ConversationHandler)

from app.bot.extension import user_battles
from app.applog import get_logger
from app.settings import Config

logger = get_logger(f"[{Config.APP_NAME}: Command Module]")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_battles.pop(update.effective_user.id, None)
        await update.message.reply_text("¡Batalla cancelada!", reply_markup=ReplyKeyboardRemove())
        logger.info("Batalla cancelada por el usuario.")
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error al cancelar la batalla: {e}")
        None