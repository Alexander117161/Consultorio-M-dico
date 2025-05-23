from utils import json_utils

class Personal:
    def __init__(self):
        self.medicos = json_utils.leer_json("personal_medicos.json") or []
        self.asistentes = json_utils.leer_json("personal_asistentes.json") or []
        self.asistencia = json_utils.leer_json("personal_asistencia.json") or {}

    def registrar_medico(self, nombre, especialidad, horario):
        medico = {
            'id': len(self.medicos) + 1,
            'nombre': nombre,
            'especialidad': especialidad,
            'horario': horario
        }
        self.medicos.append(medico)
        json_utils.guardar_json("personal_medicos.json", self.medicos)
        return medico

    def registrar_asistente(self, nombre, horario):
        asistente = {
            'id': len(self.asistentes) + 1,
            'nombre': nombre,
            'horario': horario
        }
        self.asistentes.append(asistente)
        json_utils.guardar_json("personal_asistentes.json", self.asistentes)
        return asistente

    def marcar_asistencia(self, fecha, id_personal, tipo_personal, presente=True):
        if fecha not in self.asistencia:
            self.asistencia[fecha] = {}
        key = f"{tipo_personal}_{id_personal}"
        self.asistencia[fecha][key] = presente
        json_utils.guardar_json("personal_asistencia.json", self.asistencia)

    def obtener_asistencia(self, fecha):
        return self.asistencia.get(fecha, {})

    def listar_medicos(self):
        return self.medicos

    def listar_asistentes(self):
        return self.asistentes
