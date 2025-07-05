import random
from app.core.pokemon import Pokemon
from app.data import MOVIMIENTOS_REALES


def calcular_danho(nivel, poder, atk, defensa, modificador):
    return int(((((2 * nivel / 5 + 2) * poder * atk / defensa) / 50) + 2) * modificador)

def movimientos_descripcion(poke: Pokemon, mult):
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

def aplicar_estado(objetivo: Pokemon, efecto):
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

def turno_estado(poke: Pokemon):
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