import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes)

from app.core import POKEMONES, Pokemon, movimientos_descripcion
from app.bot.extension import ELEGIR_POKEMON, ELEGIR_MOVIMIENTO, user_battles
from app.applog import get_logger
from app.settings import Config

logger = get_logger(f"[{Config.APP_NAME}: Command Module]")

async def elegir_pokemon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    choice = update.message.text.strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(POKEMONES)):
        await update.message.reply_text("¡Elige el *número* de un Pokémon válido de la lista!", parse_mode="Markdown")
        return ELEGIR_POKEMON
    idx = int(choice) - 1
    player = POKEMONES[idx]
    player = Pokemon(player.nombre, player.tipos, player.movimientos, {'ataque': player.ataque, 'defensa': player.defensa})
    rivales = [p for i, p in enumerate(POKEMONES) if i != idx]
    rival_base = random.choice(rivales)
    rival = Pokemon(rival_base.nombre, rival_base.tipos, rival_base.movimientos, {'ataque': rival_base.ataque, 'defensa': rival_base.defensa})
    ms, mo, texto_s, texto_o = player.ventaja(rival)
    user_battles[user.id] = {
        'player': player, 'rival': rival,
        'mult_player': ms, 'mult_rival': mo,
        'texto_player': texto_s, 'texto_rival': texto_o
    }
    movimientos_txt = movimientos_descripcion(player, ms)
    await update.message.reply_text(
        f"Elegiste a *{player.nombre}* ({player.tipos.capitalize()})\n"
        f"Vida: {player.barra_vida()}\n\n"
        f"Tu oponente es *{rival.nombre}* ({rival.tipos.capitalize()})\n"
        f"Vida: {rival.barra_vida()}\n\n"
        f"*Tus movimientos:*\n{movimientos_txt}\n\n"
        "Escribe o selecciona el *número* de tu movimiento:",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup([['1', '2', '3', '4']], one_time_keyboard=True)
    )
    return ELEGIR_MOVIMIENTO