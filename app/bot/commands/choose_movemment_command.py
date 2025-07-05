import random
import numpy as np
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (ContextTypes, ConversationHandler)

from app.core import movimientos_descripcion, turno_estado, aplicar_estado, calcular_danho
from app.data import MOVIMIENTOS_REALES
from app.bot.extension import ELEGIR_MOVIMIENTO, user_battles
from app.applog import get_logger
from app.settings import Config

logger = get_logger(f"[{Config.APP_NAME}: Command Module]")


async def elegir_movimiento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    choice = update.message.text.strip()
    batalla = user_battles.get(user.id)
    if not batalla:
        await update.message.reply_text("Usa /start para comenzar una batalla.")
        return ConversationHandler.END

    player = batalla['player']
    rival = batalla['rival']
    ms, mo = batalla['mult_player'], batalla['mult_rival']
    texto_s, texto_o = batalla['texto_player'], batalla['texto_rival']

    if choice not in ['1', '2', '3', '4']:
        await update.message.reply_text("Debes elegir un *número* del 1 al 4.", parse_mode="Markdown")
        return ELEGIR_MOVIMIENTO

    idx = int(choice) - 1
    mov_jugador = player.movimientos[idx]
    texto = ""

    texto_temp, salta_turno = turno_estado(player)
    texto += texto_temp
    if salta_turno:
        pass
    else:
        data = MOVIMIENTOS_REALES.get(mov_jugador, {})
        if data:
            nivel = 50
            poder = data.get('poder', 50)
            efecto = data.get('efecto', None)
            prob_efecto = data.get('prob', 0.0)
            # STAB
            stab = 1.5 if data["tipo"] == player.tipos else 1.0
            mod = stab * ms * random.uniform(0.85, 1.0)
            # Si es movimiento de curación
            if efecto == "cura":
                accion_texto = f"{player.nombre} usó {mov_jugador}. {aplicar_estado(player, 'cura')}"
            elif efecto == "drenaje":
                danho = calcular_danho(nivel, poder, player.ataque, rival.defensa, mod)
                rival.barras -= danho
                rival.barras = max(0, rival.barras)
                player.barras = min(player.ps_totales, player.barras + danho // 2)
                accion_texto = f"{player.nombre} usó {mov_jugador}. Hizo {danho} PS y recuperó {danho//2} PS."
            else:
                danho = calcular_danho(nivel, poder, player.ataque, rival.defensa, mod)
                rival.barras -= danho
                rival.barras = max(0, rival.barras)
                accion_texto = f"{player.nombre} usó {mov_jugador}. Hizo {danho} PS de daño."
                # Efecto secundario
                if efecto and random.random() < prob_efecto:
                    accion_texto += " " + aplicar_estado(rival, efecto)
        else:
            danho = int(player.ataque * ms // 4)
            rival.barras -= danho
            rival.barras = max(0, rival.barras)
            accion_texto = f"{player.nombre} usó {mov_jugador}. Hizo {danho} PS de daño."
        texto += accion_texto + f"\nVida rival: {rival.barra_vida()}\n"
        if rival.barras == 0:
            texto += f"¡{rival.nombre} se debilitó! 🎉\n"
            money = np.random.randint(1000, 5000)
            texto += f"¡Ganaste! El oponente te pagó Bs{money}."
            await update.message.reply_text(texto, reply_markup=ReplyKeyboardRemove())
            user_battles.pop(user.id, None)
            return ConversationHandler.END

    texto_temp, salta_turno_rival = turno_estado(rival)
    texto += texto_temp
    if not salta_turno_rival and rival.barras > 0:
        mov_rival = np.random.choice(rival.movimientos)
        data_rival = MOVIMIENTOS_REALES.get(mov_rival, {})
        if data_rival:
            nivel = 50
            poder = data_rival.get('poder', 50)
            efecto = data_rival.get('efecto', None)
            prob_efecto = data_rival.get('prob', 0.0)
            stab = 1.5 if data_rival["tipo"] == rival.tipos else 1.0
            mod = stab * mo * random.uniform(0.85, 1.0)
            if efecto == "cura":
                accion_texto_rival = f"{rival.nombre} usó {mov_rival}. {aplicar_estado(rival, 'cura')}"
            elif efecto == "drenaje":
                danho_rival = calcular_danho(nivel, poder, rival.ataque, player.defensa, mod)
                player.barras -= danho_rival
                player.barras = max(0, player.barras)
                rival.barras = min(rival.ps_totales, rival.barras + danho_rival // 2)
                accion_texto_rival = f"{rival.nombre} usó {mov_rival}. Hizo {danho_rival} PS y recuperó {danho_rival//2} PS."
            else:
                danho_rival = calcular_danho(nivel, poder, rival.ataque, player.defensa, mod)
                player.barras -= danho_rival
                player.barras = max(0, player.barras)
                accion_texto_rival = f"{rival.nombre} usó {mov_rival}. Hizo {danho_rival} PS de daño."
                if efecto and random.random() < prob_efecto:
                    accion_texto_rival += " " + aplicar_estado(player, efecto)
        else:
            danho_rival = int(rival.ataque * mo // 4)
            player.barras -= danho_rival
            player.barras = max(0, player.barras)
            accion_texto_rival = f"{rival.nombre} usó {mov_rival}. Hizo {danho_rival} PS de daño."
        texto += accion_texto_rival + f"\nVida tuya: {player.barra_vida()}\n"
        if player.barras == 0:
            texto += f"¡{player.nombre} se debilitó! 😢\nHas perdido la batalla."
            await update.message.reply_text(texto, reply_markup=ReplyKeyboardRemove())
            user_battles.pop(user.id, None)
            return ConversationHandler.END

    movimientos_txt = movimientos_descripcion(player, ms)
    texto += (
        f"\nEstado de {player.nombre}: {player.estado}\n"
        f"Estado de {rival.nombre}: {rival.estado}\n"
        "\nSelecciona el *número* de tu siguiente movimiento:\n" + movimientos_txt
    )
    await update.message.reply_text(
        texto,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup([['1', '2', '3', '4']], one_time_keyboard=True)
    )
    return ELEGIR_MOVIMIENTO