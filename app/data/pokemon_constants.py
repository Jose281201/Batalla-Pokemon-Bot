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