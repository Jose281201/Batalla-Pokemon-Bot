import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, ConversationHandler
)
import numpy as np

# --- Lógica de Pokémon adaptada ---
class Pokemon:
    def __init__(self, nombre, tipos, movimientos, EVs):
        self.nombre = nombre
        self.tipos = tipos
        self.movimientos = movimientos
        self.ataque = EVs['ataque']
        self.defensa = EVs['defensa']
        self.barras = 20  # Salud máxima

    def ventaja(self, otro):
        version = ['fuego', 'agua', 'planta']
        mult_self, mult_otro = 1, 1
        texto_self, texto_otro = '', ''
        for i, k in enumerate(version):
            if self.tipos == k:
                if otro.tipos == k:
                    texto_self = texto_otro = 'No es muy efectivo…'
                elif otro.tipos == version[(i+1)%3]:  # Desventaja
                    mult_otro, mult_self = 2, 0.5
                    texto_self = 'No es muy efectivo…'
                    texto_otro = '¡Es muy eficaz!'
                elif otro.tipos == version[(i+2)%3]:  # Ventaja
                    mult_self, mult_otro = 2, 0.5
                    texto_self = '¡Es muy eficaz!'
                    texto_otro = 'No es muy efectivo…'
                break
        return mult_self, mult_otro, texto_self, texto_otro

# --- Diccionario para guardar el estado de batalla de cada usuario ---
user_battles = {}

# --- Estados de la conversación ---
ELEGIR = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Instancia Pokémon (reinicia batalla)
    player = Pokemon('Charizard', 'fuego', ['Lanzallamas', 'Pirotecnia', 'Giro Fuego', 'Carga de Fuego'], {'ataque':12, 'defensa':8})
    rival = Pokemon('Blastoise', 'agua', ['Cascada', 'Surf', 'Hidrobomba', 'Hidropulso'], {'ataque':10, 'defensa':10})
    ms, mo, texto_s, texto_o = player.ventaja(rival)

    # Guarda estado de batalla
    user_battles[user.id] = {
        'player': player, 'rival': rival,
        'mult_player': ms, 'mult_rival': mo,
        'texto_player': texto_s, 'texto_rival': texto_o
    }

    await update.message.reply_text(
        "¡Comienza la batalla!\n\n"
        "Tus datos:\n"
        f"{player.nombre} (Tipo: {player.tipos})\n"
        f"Movimientos: {', '.join(player.movimientos)}\n\n"
        "Tu rival:\n"
        f"{rival.nombre} (Tipo: {rival.tipos})\n"
        "¡Elige tu movimiento!",
        reply_markup=ReplyKeyboardMarkup([[m] for m in player.movimientos], one_time_keyboard=True)
    )
    return ELEGIR

async def elegir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    choice = update.message.text
    batalla = user_battles.get(user.id)
    if not batalla:
        await update.message.reply_text("Usa /start para comenzar una batalla.")
        return ConversationHandler.END

    player = batalla['player']
    rival = batalla['rival']
    ms, mo = batalla['mult_player'], batalla['mult_rival']
    texto_s, texto_o = batalla['texto_player'], batalla['texto_rival']

    if choice not in player.movimientos:
        await update.message.reply_text("Elige un movimiento válido.")
        return ELEGIR

    # Turno del jugador
    daño = int(player.ataque * ms)
    rival.barras -= daño
    rival.barras = max(0, rival.barras)
    texto = (
        f"¡{player.nombre} usó {choice}!\n{texto_s}\n"
        f"{rival.nombre} ahora tiene {'█'*rival.barras}{' '*(20-rival.barras)} ({rival.barras}/20 PS)\n"
    )
    if rival.barras == 0:
        texto += f"¡{rival.nombre} se debilitó! 🎉\n"
        money = np.random.randint(1000, 5000)
        texto += f"¡Ganaste! El oponente te pagó Bs{money}."
        await update.message.reply_text(texto, reply_markup=ReplyKeyboardRemove())
        user_battles.pop(user.id, None)
        return ConversationHandler.END

    # Turno del rival (aleatorio)
    mov_rival = np.random.choice(rival.movimientos)
    daño_rival = int(rival.ataque * mo)
    player.barras -= daño_rival
    player.barras = max(0, player.barras)
    texto += (
        f"¡{rival.nombre} usó {mov_rival}!\n{texto_o}\n"
        f"{player.nombre} ahora tiene {'█'*player.barras}{' '*(20-player.barras)} ({player.barras}/20 PS)\n"
    )
    if player.barras == 0:
        texto += f"¡{player.nombre} se debilitó! 😢\nHas perdido la batalla."
        await update.message.reply_text(texto, reply_markup=ReplyKeyboardRemove())
        user_battles.pop(user.id, None)
        return ConversationHandler.END

    texto += "\n¡Elige tu siguiente movimiento!"
    await update.message.reply_text(
        texto,
        reply_markup=ReplyKeyboardMarkup([[m] for m in player.movimientos], one_time_keyboard=True)
    )
    return ELEGIR

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_battles.pop(update.effective_user.id, None)
    await update.message.reply_text("¡Batalla cancelada!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    # Activa logs (opcional)
    logging.basicConfig(level=logging.INFO)
    TOKEN = "7868989127:AAFY47qJ504pgpFctnec2zTXEaLjsFDEDY4"  # - Pega aquí tu token
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={ELEGIR: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir)]},
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler('cancel', cancel))
    print("Bot corriendo. ¡Inicia la batalla en Telegram con /start!")
    app.run_polling()

if __name__ == '__main__':
    main()