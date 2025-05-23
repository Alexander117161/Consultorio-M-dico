import csv
import os

def cargar_puebla_municipios():
    ruta = os.path.join(os.path.dirname(__file__), '..', 'base_datos', 'puebla_municipios.csv')
    juntas = set()
    with open(ruta, newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            juntas.add(fila['Comunidad'].strip().lower())
    return juntas

def comunidad_es_valida(comunidad):
    juntas = cargar_puebla_municipios()
    return comunidad.strip().lower() in juntas
