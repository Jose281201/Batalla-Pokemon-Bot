from telegram import Update
from telegram.ext import (ContextTypes)

from app.applog import get_logger
from app.settings import Config

logger = get_logger(f"[{Config.APP_NAME}: Command Module]")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *Comandos disponibles:*\n\n"
        "/start - Inicia una batalla Pokémon y muestra las opciones a elegir\n"
        "/help - Muestra esta ayuda de comandos\n"
        "/cancel - Cancela la batalla actual\n\n"
        "Durante la batalla, selecciona Pokémon y movimientos respondiendo con el *número* correspondiente.",
        parse_mode="Markdown"
    )