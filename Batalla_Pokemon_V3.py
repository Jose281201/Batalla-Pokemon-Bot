import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, ConversationHandler
)
import numpy as np
import random

# Datos reales de movimientos Pokémon (puedes ampliar esta tabla)
MOVIMIENTOS_REALES = {
    "Lanzallamas": {"tipo": "fuego", "poder": 90, "efecto": "quemar", "prob": 0.1},
    "Pirotecnia": {"tipo": "fuego", "poder": 70, "efecto": None, "prob": 0.0},
    "Giro Fuego": {"tipo": "fuego", "poder": 35, "efecto": "quemar", "prob": 0.1},
    "Carga de Fuego": {"tipo": "fuego", "poder": 50, "efecto": None, "prob": 0.0},

    "Surf": {"tipo": "agua", "poder": 90, "efecto": None, "prob": 0.0},
    "Cascada": {"tipo": "agua", "poder": 80, "efecto": "retroceder", "prob": 0.2},
    "Hidrobomba": {"tipo": "agua", "poder": 110, "efecto": None, "prob": 0.0},
    "Hidropulso": {"tipo": "agua", "poder": 60, "efecto": "confundir","prob": 0.2},

    "Latigo cepa": {"tipo": "planta","poder": 45, "efecto": None, "prob": 0.0},
    "Hoja Afilada": {"tipo": "planta","poder": 55, "efecto": None, "prob": 0.0},
    "Rayo Solar": {"tipo": "planta","poder": 120, "efecto": None, "prob": 0.0},
    "Abatidoras": {"tipo": "planta","poder": 75, "efecto": "drenaje", "prob": 1.0},

    "Impactrueno": {"tipo": "eléctrico","poder": 40, "efecto": "paralizar", "prob": 0.1},
    "Rayo": {"tipo": "eléctrico","poder": 90, "efecto": "paralizar", "prob": 0.1},
    "Chispa": {"tipo": "eléctrico","poder": 65, "efecto": "paralizar", "prob": 0.3},
    "Placaje Electrico": {"tipo": "eléctrico","poder": 120, "efecto": "paralizar", "prob": 0.1},

    "Golpe Cuerpo": {"tipo": "normal", "poder": 85, "efecto": "paralizar", "prob": 0.3},
    "Descanso": {"tipo": "normal", "poder": 0, "efecto": "cura", "prob": 1.0},
    "Hiperrayo": {"tipo": "normal", "poder": 150,"efecto": None, "prob": 0.0},
    "Placaje": {"tipo": "normal", "poder": 40, "efecto": None, "prob": 0.0},

    "Psicorrayo": {"tipo": "psíquico", "poder": 65, "efecto": "confundir", "prob": 0.1},
    "Confusión": {"tipo": "psíquico", "poder": 50, "efecto": "confundir", "prob": 0.1},
    "Poder Pasado": {"tipo": "roca", "poder": 60, "efecto": None, "prob": 0.0},
    "Recuperación": {"tipo": "psíquico", "poder": 0, "efecto": "cura", "prob": 1.0},

    "Lanzarrocas": {"tipo": "roca", "poder": 50, "efecto": None, "prob": 0.0},
    "Excavar": {"tipo": "tierra", "poder": 80, "efecto": None, "prob": 0.0},
    "Afilagarras": {"tipo": "roca", "poder": 0, "efecto": None, "prob": 0.0},
    "Terremoto": {"tipo": "tierra", "poder": 100, "efecto": None, "prob": 0.0},
    "Avalancha": {"tipo": "roca", "poder": 75, "efecto": None, "prob": 0.0},
    "Puño Fuego": {"tipo": "fuego", "poder": 75, "efecto": "quemar", "prob": 0.1},
    "Roca Afilada": {"tipo": "roca", "poder": 100, "efecto": None, "prob": 0.0},

    "Ataque Ala": {"tipo": "volador", "poder": 60, "efecto": None, "prob": 0.0},
    "Tornado": {"tipo": "volador", "poder": 40, "efecto": None, "prob": 0.0},
    "Doble Equipo": {"tipo": "normal", "poder": 0, "efecto": None, "prob": 0.0},
    "Golpe Aéreo": {"tipo": "volador", "poder": 120,"efecto": None, "prob": 0.0},

    "Canto Helado": {"tipo": "hielo", "poder": 55, "efecto": "dormir", "prob": 0.1},
    "Rayo Hielo": {"tipo": "hielo", "poder": 90, "efecto": "congelar", "prob": 0.1},
    "Cabeza de Hierro": {"tipo": "acero", "poder": 80, "efecto": "retroceder", "prob": 0.3},
}

PS_POKEMON = {
    "Charizard": 156, "Blastoise": 158, "Venusaur": 160, "Pikachu": 100, "Snorlax": 267,
    "Alakazam": 135, "Onix": 97, "Golem": 150, "Pidgeot": 158, "Lapras": 210
}

ESTADOS = ["normal", "dormido", "paralizado", "quemado", "congelado", "confundido"]

def calcular_danho(nivel, poder, atk, defensa, modificador):
    return int(((((2 * nivel / 5 + 2) * poder * atk / defensa) / 50) + 2) * modificador)

class Pokemon:
    def __init__(self, nombre, tipos, movimientos, EVs):
        self.nombre = nombre
        self.tipos = tipos
        self.movimientos = movimientos
        self.ataque = EVs['ataque']
        self.defensa = EVs['defensa']
        self.ps_totales = PS_POKEMON[nombre]
        self.barras = self.ps_totales
        self.estado = "normal"
        self.turnos_estado = 0

    def barra_vida(self):
        bloques = int((self.barras / self.ps_totales) * 20)
        return f"{'█'*bloques}{' '*(20-bloques)} ({self.barras}/{self.ps_totales} PS)"

    def ventaja(self, otro):
        efectividad = {
            'fuego': {'planta': 2, 'hielo': 2, 'bicho': 2, 'acero': 2, 'fuego': 0.5, 'agua': 0.5, 'roca': 0.5, 'dragón': 0.5},
            'agua': {'fuego': 2, 'roca': 2, 'tierra': 2, 'agua': 0.5, 'planta': 0.5, 'dragón': 0.5},
            'planta': {'agua': 2, 'roca': 2, 'tierra': 2, 'fuego': 0.5, 'planta': 0.5, 'volador': 0.5, 'bicho': 0.5, 'veneno': 0.5, 'dragón': 0.5, 'acero': 0.5},
            'eléctrico': {'agua': 2, 'volador': 2, 'eléctrico': 0.5, 'planta': 0.5, 'tierra': 0, 'dragón': 0.5},
            'normal': {'roca': 0.5, 'acero': 0.5, 'fantasma': 0},
            'psíquico': {'lucha': 2, 'veneno': 2, 'psíquico': 0.5, 'acero': 0.5, 'siniestro': 0},
            'roca': {'fuego': 2, 'hielo': 2, 'volador': 2, 'bicho': 2, 'lucha': 0.5, 'tierra': 0.5, 'acero': 0.5},
            'tierra': {'fuego': 2, 'eléctrico': 2, 'roca': 2, 'acero': 2, 'planta': 0.5, 'bicho': 0.5},
            'volador': {'planta': 2, 'lucha': 2, 'bicho': 2, 'eléctrico': 0.5, 'roca': 0.5, 'acero': 0.5},
            'hielo': {'planta': 2, 'tierra': 2, 'volador': 2, 'dragón': 2, 'fuego': 0.5, 'agua': 0.5, 'hielo': 0.5, 'acero': 0.5},
        }
        self_type = self.tipos
        other_type = otro.tipos
        mult_self = efectividad.get(self_type, {}).get(other_type, 1)
        mult_otro = efectividad.get(other_type, {}).get(self_type, 1)
        texto_self = "¡Es muy eficaz!" if mult_self > 1 else ("No es muy efectivo..." if mult_self < 1 else "")
        texto_otro = "¡Es muy eficaz!" if mult_otro > 1 else ("No es muy efectivo..." if mult_otro < 1 else "")
        if mult_self == 0:
            texto_self = "¡No afecta al rival!"
        if mult_otro == 0:
            texto_otro = "¡No te afecta!"
        return mult_self, mult_otro, texto_self, texto_otro

POKEMONES = [
    Pokemon('Charizard', 'fuego', ['Lanzallamas', 'Pirotecnia', 'Giro Fuego', 'Carga de Fuego'], {'ataque':84, 'defensa':78}),
    Pokemon('Blastoise', 'agua', ['Cascada', 'Surf', 'Hidrobomba', 'Hidropulso'], {'ataque':83, 'defensa':100}),
    Pokemon('Venusaur', 'planta', ['Latigo cepa', 'Hoja Afilada', 'Rayo Solar', 'Abatidoras'], {'ataque':82, 'defensa':83}),
    Pokemon('Pikachu', 'eléctrico', ['Impactrueno', 'Rayo', 'Chispa', 'Placaje Electrico'], {'ataque':55, 'defensa':40}),
    Pokemon('Snorlax', 'normal', ['Golpe Cuerpo', 'Descanso', 'Hiperrayo', 'Placaje'], {'ataque':110, 'defensa':65}),
    Pokemon('Alakazam', 'psíquico', ['Psicorrayo', 'Confusión', 'Poder Pasado', 'Recuperación'], {'ataque':50, 'defensa':45}),
    Pokemon('Onix', 'roca', ['Lanzarrocas', 'Excavar', 'Afilagarras', 'Placaje'], {'ataque':45, 'defensa':160}),
    Pokemon('Golem', 'tierra', ['Terremoto', 'Avalancha', 'Puño Fuego', 'Roca Afilada'], {'ataque':120, 'defensa':130}),
    Pokemon('Pidgeot', 'volador', ['Ataque Ala', 'Tornado', 'Doble Equipo', 'Golpe Aéreo'], {'ataque':80, 'defensa':75}),
    Pokemon('Lapras', 'hielo', ['Canto Helado', 'Rayo Hielo', 'Surf', 'Cabeza de Hierro'], {'ataque':85, 'defensa':80}),
]

user_battles = {}
ELEGIR_POKEMON, ELEGIR_MOVIMIENTO = range(2)

def movimientos_descripcion(poke, mult):
    descripciones = []
    for i, mov in enumerate(poke.movimientos):
        data = MOVIMIENTOS_REALES.get(mov)
        if data:
            desc = f"Poder: {data['poder']}"
            if data['prob'] and data['efecto']:
                desc += f", {int(data['prob']*100)}% de {data['efecto']}"
            elif data['efecto'] == "cura":
                desc = "Recupera 50% de PS"
            descripciones.append(f"{i+1}. {mov} — {desc}")
        else:
            descripciones.append(f"{i+1}. {mov}")
    return "\n".join(descripciones)

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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *Comandos disponibles:*\n\n"
        "/start - Inicia una batalla Pokémon y muestra las opciones a elegir\n"
        "/help - Muestra esta ayuda de comandos\n"
        "/cancel - Cancela la batalla actual\n\n"
        "Durante la batalla, selecciona Pokémon y movimientos respondiendo con el *número* correspondiente.",
        parse_mode="Markdown"
    )

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

def aplicar_estado(objetivo, efecto):
    if efecto == "cura":
        curado = int(objetivo.ps_totales // 2)
        objetivo.barras = min(objetivo.ps_totales, objetivo.barras + curado)
        return f"Recuperó {curado} PS."
    elif efecto == "dormir":
        objetivo.estado = "dormido"
        objetivo.turnos_estado = 2
        return "Quedó dormido."
    elif efecto == "paralizar":
        objetivo.estado = "paralizado"
        objetivo.turnos_estado = 3
        return "Ahora está paralizado."
    elif efecto == "quemar":
        objetivo.estado = "quemado"
        objetivo.turnos_estado = 3
        return "¡Está quemado!"
    elif efecto == "drenaje":
        drenado = min(40, objetivo.barras)
        objetivo.barras -= drenado
        return f"Le drenaron {drenado} PS."
    return ""

def turno_estado(poke):
    texto = ""
    if poke.estado == "dormido":
        poke.turnos_estado -= 1
        if poke.turnos_estado > 0:
            texto += f"{poke.nombre} está dormido y no puede atacar.\n"
            return texto, True
        else:
            poke.estado = "normal"
            texto += f"{poke.nombre} se despertó.\n"
    elif poke.estado == "paralizado":
        poke.turnos_estado -= 1
        if random.random() < 0.5 and poke.turnos_estado > 0:
            texto += f"{poke.nombre} está paralizado y no puede moverse.\n"
            return texto, True
        if poke.turnos_estado <= 0:
            poke.estado = "normal"
            texto += f"{poke.nombre} ya no está paralizado.\n"
    elif poke.estado == "quemado":
        poke.barras -= int(poke.ps_totales*0.06)
        poke.barras = max(0, poke.barras)
        poke.turnos_estado -= 1
        texto += f"{poke.nombre} está quemado y pierde PS.\n"
        if poke.turnos_estado <= 0:
            poke.estado = "normal"
            texto += f"{poke.nombre} ya no está quemado.\n"
    return texto, False

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

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_battles.pop(update.effective_user.id, None)
    await update.message.reply_text("¡Batalla cancelada!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    logging.basicConfig(level=logging.INFO)
    TOKEN = "7868989127:AAFY47qJ504pgpFctnec2zTXEaLjsFDEDY4"
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ELEGIR_POKEMON: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir_pokemon)],
            ELEGIR_MOVIMIENTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir_movimiento)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('cancel', cancel))
    print("Bot corriendo. ¡Inicia la batalla en Telegram con /start!")
    app.run_polling()

if __name__ == '__main__':
    main()