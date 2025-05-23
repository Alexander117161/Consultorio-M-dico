import json
import os

def leer_json(ruta, valor_por_defecto=None):
    if not os.path.exists(ruta):
        return valor_por_defecto
    with open(ruta, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return valor_por_defecto


def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
