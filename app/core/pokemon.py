from app.data import PS_POKEMON

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