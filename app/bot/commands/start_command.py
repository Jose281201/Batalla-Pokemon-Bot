from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes)

from app.core import POKEMONES
from app.bot.extension import ELEGIR_POKEMON
from app.applog import get_logger
from app.settings import Config

logger = get_logger(f"[{Config.APP_NAME}: Command Module]")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pokemon_info = "\n".join([f"{i+1}. {p.nombre} ({p.tipos.capitalize()}) [{p.ps_totales} PS]" for i, p in enumerate(POKEMONES)])
    await update.message.reply_text(
        f"¡Bienvenido a la batalla Pokémon!\n\n"
        f"Pokémon disponibles para elegir:\n{pokemon_info}\n\n"
        "¿Qué Pokémon eliges? Escribe o selecciona el *número*.",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup([[str(i+1)] for i in range(len(POKEMONES))], one_time_keyboard=True)
    )
    return ELEGIR_POKEMON